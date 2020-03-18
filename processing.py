def find_rawTokens(inStr, knowledgeProcessor):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    Looks for both full tokens from knowledgeSet and single-word (sub) tokens
    """
    # use greedy matching of flashtext algorithm to find keywords
    greedyTokens = list(knowledgeProcessor.extract_keywords(inStr))
    # initialize list of all tokens with greedy tokens
    allTokens = greedyTokens.copy()
    # iterate over greedy tokens
    for token in greedyTokens:
        splitToken = token.split()
        if not (len(splitToken)==1):
            # iterate over white-space delimited words in each token
            for word in token.split():
                # find all tokens within the word and add to all tokens
                smallTokens = knowledgeProcessor.extract_keywords(word)
                allTokens += smallTokens
    return allTokens
