class Article(object):
    def __init__(self, j):
        self.id = j['paper_id']
        meta = j['metadata']
        self.title = meta['title']
        self.abstract = j['abstract']

    def __str__(self):
        return f'<{self.title}>'


# class Database(object):
    # def __init__(self):
