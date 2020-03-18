import re
from unidecode import unidecode

## Matchers ##
# matches non-alphanumeric, space, or sentence-ending punctuation (dash must be at end)
stripMatcher = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
# matches any sequence of tabs, newlines, spaces, underscores, and dashes
spaceMatcher = re.compile(r'[\t\n\s_:;/<>*&^%$#@()"~`+-]+')
# matches \t \r and \n in titles
slashMatcher = re.compile(r".\r|.\n|.\t")


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
    # detach sentence-ending punc from last words
    detachedString = re.sub(r"(?<=[a-zA-z])(?P<punc>[.!?])(?=(\s[a-zA-Z]|$))",
                            " \g<punc>", spacedString)
    # lowercase the alpha chars that remain
    loweredString = detachedString.lower()
    return loweredString


def clean_title(rawTitle):
    """
    Cleans title of webpage, removing large spaces and junk while
    preserving valid punctuation, numbers, and capitalization.
    """
    deslashedTitle = re.sub(slashMatcher, "", rawTitle)
    spacedTitle = re.sub(spaceMatcher, " ", deslashedTitle).strip()
    return spacedTitle
