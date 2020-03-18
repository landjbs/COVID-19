"""
Functions for all text processing involding knowledgeSet and tokenizer
built in models.knowledge.knowledgeBuilder.
"""

import re
import math
from numpy import log
from collections import Counter


# dict mapping html divs to score  multiplier
divMultipiers = {'title':           5,
                'abstract':         6,
                'body':             5}


def find_rawTokens(inStr, tokenizer):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    Looks for both full tokens from knowledgeSet and single-word (sub) tokens
    """
    # use greedy matching of flashtext algorithm to find keywords
    greedyTokens = list(tokenizer.extract_keywords(inStr))
    # initialize list of all tokens with greedy tokens
    allTokens = greedyTokens.copy()
    # iterate over greedy tokens
    for token in greedyTokens:
        splitToken = token.split()
        if not (len(splitToken)==1):
            # iterate over white-space delimited words in each token
            for word in token.split():
                # find all tokens within the word and add to all tokens
                smallTokens = tokenizer.extract_keywords(word)
                allTokens += smallTokens
    return allTokens


def DEPRECATED_find_weighted_tokenCounts(inStr, tokenizer):
    """
    DEPRECATED
    Finds dict mapping tokens used in inStr to number of times used.
    Does not normalize by length, div, or average frequency.
    """
    # get multi-occurence list of the greedy tokens in inStr
    greedyTokens = tokenizer.extract_keywords(inStr)
    # get multi-occurence list of sub tokens in ' '-split greed tokens
    subTokens = []
    for token in greedyTokens:
        splitToken = token.split()
        if not (len(splitToken)==1):
            for word in splitToken:
                subTokens += tokenizer.extract_keywords(word)
    # get counts of sub tokens and normalize by 0.7
    weightedSubCounter = {token:(0.7*count)
                            for token, count in Counter(subTokens).items()}
    # combine greedTokens and normalized subTokens to get weighted token counts
    countedTokens = Counter(greedyTokens)
    countedTokens.update(weightedSubCounter)
    return countedTokens


def find_weighted_tokenCounts(text, tokenizer, maxChunkSize=5):
    """
    Finds dict mapping tokens used in inStr to number of times used.
    Does not normalize by length, div, or average frequency.
    Sub-tokens are weighted by the fraction of the greedy-token they take up
    Args:
        -text:                      Raw text of the div
        -tokenizer:        Greedy-first flashtext processor
        -maxChunkSize:              Highest number of " "-split words to allow
                                        in a sub-token chunk. Greedy, top-tokens
                                        will be added, no matter the length.
    Returns:
        Counter() of greedy tokens and subtokens. Greedy-tokens are mapped to
        their raw count in the text; sub-tokens are mapped to their occurence
        in the text times the fraction of the greedy token they take up.
    """
    # find list of greedy tokens in text
    greedyTokens = Counter(tokenizer.extract_keywords(text))
    subTokens = Counter()
    # iterate over greedy list
    for greedyToken, greedyCount in greedyTokens.items():
        greedyWords = greedyToken.split()
        wordNum = len(greedyWords)
        # if multiple words in cur topToken, recursively look for sub tokens
        if wordNum > 1:
            # init chunk is 1 smaller than wordNum but capped at maxChunkSize
            chunkSize = min(maxChunkSize, (wordNum - 1))
            # iterate over greedy tokens, analyzing smaller chunks at a time
            while chunkSize > 0:
                for i in range(wordNum):
                    chunkWords = greedyWords[i : i+chunkSize]
                    textChunk = ' '.join(chunkWords)
                    # if the chunk is a token in the tokenizer,
                    # add its count tokenCounts after norming by fraction
                    # of larger token and multiplying by larger token's count
                    # (becuase you're iterating over a set)
                    if textChunk in tokenizer:
                        subTokens.update({textChunk :
                                            (greedyCount * (len(chunkWords)
                                                            / wordNum))})
                chunkSize -= 1
    greedyTokens.update(subTokens)
    return greedyTokens


def score_token(token, observedTokenFreq, multiplier, freqDict):
    """
    Scores individual token in a div by frequency, multiplier, and distribution
    """
    ### NORMALIZE TOKEN FREQUENCY ###
    # get term and document frequency of token in freqDict built on scraped data
    try:
        termFreq, inverseDocFreq = freqDict[token]
    except:
        termFreq, inverseDocFreq = 0, 0
    # normalize tokenFreq using a tf-idf schema
    normedFreq = observedTokenFreq - (1.2 * termFreq)
    # tokens with negative normedFreq will automatically have scores of 0
    if normedFreq <= 0:
        return 0
    ### Apply specialMultiplier ###
    score = normedFreq * multiplier
    return round(score, 3)


def find_scoredTokens(divText, div, tokenizer, freqDict, cutoff):
    """
    Args:
        divText:                Text of division being analyzed
        div:                    Name of division being analyzed
        tokenizer:     Greedy-first flashtext processor
        freqDict:               Dict of average word frequencies
        cutoff:                 Score cutoff to include token in dict
    Returns:
        Dict of tokens in divText mapping to score assigned by score_token
    """

    # find multiplier related to div
    divMultipier = divMultipiers[div]

    # use tokenizer to extract weighted token counts from divText
    weightedTokenCounts = find_weighted_tokenCounts(divText, tokenizer)

    # find number of words in divText or (if url) number chars/(avg word len)
    if div=='url':
        divLen = len(divText) / 5
    else:
        divLen = len(divText.split())

    multiplier = divMultipier

    # apply div specific scoring
    # if (div=='all'):
    #     ### TOKEN DISTRIBUTION SCORING ###
    #     # find start and end location of each token usage in the text
    #     # tokenLocs = [(loc.span()[0], loc.span()[1]) for loc in re.finditer(token, divText, flags=re.IGNORECASE)]
    #     # get loc of first token usage
    #     # firstUse = tokenLocs[0]
    #     # give benefit to pages with tokens appearing early
    #     ### RELATIVE LENGTH SCORING ###
    #     # get page length relative to average word count (assumed 700)
    #     relativeLen = divLen / 700
    #     # use sigmoid function on relative length to benefit longer pages with equal token freq to shorter (multiplier asymptotes at 1 and ~5)
    #     lengthMultiplier = (math.exp(0.25 * relativeLen) / (math.exp(0.25 * (relativeLen - 5.2)) + 1)) + 1
    #     specialMultiplier = lengthMultiplier
    # else:
    #     specialMultiplier = 0

    # create dict mapping tokens to scores as function of frequency
    tokenScores = {token:score_token(token=token,
                                    observedTokenFreq=(weightedCount/divLen),
                                    multiplier=multiplier,
                                    freqDict=freqDict)
                    for token, weightedCount in weightedTokenCounts.items()}
    # filter scores below cuoff
    filteredScores = {token: score for token, score in tokenScores.items()
                        if score > cutoff}
    return filteredScores


def score_divDict(divDict, tokenizer, freqDict):
    """
    Args: Dict mapping page divisions to cleaned content (eg. {'title':'foo',
    'all':'hello world'}), tokenizer to use for matching, and dict of
    average knowledge token frequency.
    Returns: Dict mapping all knowledge tokens found in divDict to score
    determined by div found and relative frequency.
    """
    # initialize Counter to hold tokens mapping to sum scores across all divs
    scoreCounter = Counter()
    # iterate over divisions in divDict
    for div in divDict:
        # get dict mapping tokens in divText to thier scores
        divScores = find_scoredTokens(divText=divDict[div],
                                        div=div,
                                        tokenizer=tokenizer,
                                        freqDict=freqDict,
                                        cutoff=0.002)
        scoreCounter.update(divScores)
    return scoreCounter
