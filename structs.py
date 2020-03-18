import re
from unidecode import unidecode
from flashtext import KeywordProcessor


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
    detachedString = re.sub(r"(?<=[a-zA-z])(?P<punc>[.!?])(?=(\s[A-Z]*|\b))",
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


class Article(object):
    def __init__(self, j):
        self.id = j['paper_id']
        meta = j['metadata']
        self.title = clean_title(meta['title'])
        abstract = j['abstract']
        self.abstract = abstract if (abstract!=[]) else None
        self.paragraphs = []
        for paragraph in j['body_text']:
            self.paragraphs.append(clean_text(paragraph['text']))

    def __str__(self):
        return f'<{self.title}>'

    def display(self):
        print(self.title)
        print('\n'.join(self.paragraphs))


class Database(object):
    def __init__(self):
        # build text matcher for tokens
        tokens = ['co-infection']
        knowledgeSet = {clean_text(s) for s in tokens}
        knowledgeProcessor = KeywordProcessor(case_sensitive=False)
        for i, keyword in enumerate(knowledgeSet):
            knowledgeProcessor.add_keyword(keyword)


    def read_articles(self):
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
                            yield article_obj
