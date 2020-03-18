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


class Article(object):
    def __init__(self, j):
        self.id = j['paper_id']
        meta = j['metadata']
        self.title = meta['title']
        abstract = j['abstract']
        self.abstract = abstract if (abstract!=[]) else None
        self.paragraphs = []
        for paragraph in j['body_text']:
            self.paragraphs.append(paragraph['text'])

    def __str__(self):
        return f'<{self.title}>'

    def display(self):
        print(self.title)
        print('\n'.join(self.paragraphs))


class Database(object):
    def __init__(self):
        keywords = ['co-infections']
