'''
File processing to load database
'''


import os
import json
from tqdm import tqdm

from structs import Article


file_folders = ['bioxiv_medrxiv', 'comm_use_subset',
                'noncomm_use_subset', 'pmc_custom_license']


for top_folder in tqdm(os.listdir('2020-03-13')):
    if top_folder in file_folders:
        for path in os.listdir(f'2020-03-13/{top_folder}/{top_folder}'):
            if path.endswith('.json'):
                path = f'2020-03-13/{top_folder}/{top_folder}/{path}'
                with open(path, 'r') as load_file:
                    article_json = json.load(load_file)
                    article_obj = Article(article_json)
                    article_obj.display()

import re
from unidecode import unidecode


# converts anything that looks like a year range (eg. 1910-11) into two years (eg. 1910 1911)
# rangedString = re.sub(r'\b(?P<firstTwo>[0-9]{2})(?P<secondTwo>[0-9]{2})-(?P<lastTwo>[0-9]{2}) ', "\g<firstTwo>\g<secondTwo> \g<firstTwo>\g<lastTwo>", dewikiedWiki)

# def convert_ordinal_number(inStr):
#     """
#     Converts ordinal numbers (eg. 1st) to their english
#     representation (eg. first)
#     """
#


## Functions ##
def clean_text(rawString):
    """
    Cleans rawString by replacing spaceMatcher and tagMatcher with a single
    space, removing non-alpha chars, and lowercasing alpha chars
    """
    # replace accented characters with non-accent representation
    deaccentedString = unidecode(rawString)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", rawString)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(spaceMatcher, " ", cleanedString).strip()
    # lowercase the alpha chars that remain
    loweredString = spacedString.lower()
    return loweredString


def clean_web_text(rawWebText):
    """ Cleans web text by removing tags and then feeding into clean_text """
    # replace html tags with " "
    detaggedString = re.sub(tagMatcher, " ", rawWebText)
    return clean_text(detaggedString)


def clean_wiki(rawWiki):
    """
    Cleans wikipedia title during knowledgeSet construction. Wraps clean_text
    but removes special wikipedia words like '(disambiguation)'.
    """
    # remove special wiki words
    dewikiedWiki = re.sub(wikiMatcher, "", rawWiki)
    # use clean_text to do the rest
    cleanedWiki = clean_text(dewikiedWiki)
    return cleanedWiki


def clean_title(rawTitle):
    """
    Cleans title of webpage, removing large spaces and junk while
    preserving valid punctuation, numbers, and capitalization.
    """
    deslashedTitle = re.sub(slashMatcher, "", rawTitle)
    spacedTitle = re.sub(spaceMatcher, " ", deslashedTitle).strip()
    return spacedTitle


def clean_url(rawURL):
    """
    Cleans url for knowledge tokenization by stripping punctuation and removing
    http, www, com, etc. Not to be confused with urlAnalyzer.fix_url!
    """
    cleanedURL = re.sub(urlMatcher, "", rawURL)
    strippedURL = re.sub(stripMatcher, "", cleanedURL)
    return strippedURL


def clean_file_name(rawFileName):
    """ Cleans name of a file """
    detypedFileName = re.sub(fileMatcher, "", rawFileName)
    return clean_text(detypedFileName)


### SEARCH CLEANERS ###
# dictionary to find english form of punctuation in search conversion
puncDict = {'.':'period', ',':'comma', '!':'exclamation mark',
            '?':'question mark', '...':'ellipses', '"':'quotation mark',
            "'":'appostrophe', ':':'colon', ';':'semicolon', '&':'ampersand',
            '=':'equals', '{':'bracket', '}':'bracket', '+':'plus', '-':'minus',
            '=':'equals','~':'tilda', '$':'dollar sign',
            '[':'square bracket', ']':'square bracket', '%':'percent',
            '_':'underscore'}

puncDict = {'.':'period'}


puncMatcher = re.compile(("|".join([punc for punc in puncDict.keys()])))

def clean_search(rawSearch):
    """
    Cleans search for spelling correction and tokenization.
    Wraps clean_text, but solo punctuation is converted to english
    form rather than removed (eg. : meaning -> colon meaning)
    """
    # to fix
    # puncSubbed = re.sub(r"?P<punc>{puncMatcher}", puncDict['\g<punc>'], rawSearch)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", rawSearch)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(searchSpaceMatcher, " ", cleanedString).strip()
    # lowercase the alpha chars that remain
    loweredString = spacedString.lower()
    return loweredString


def end_test(rawString):
    """ Adds space before sentence-ending punctuation. Not yet used. """
    return re.sub(r"(?<=[a-zA-z])(?P<punc>[.!?])(?=\s[A-Z])", " \g<punc>", rawString)
