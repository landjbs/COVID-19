class Article(object):
    def __init__(self, j):
        self.id = j['paper_id']
        meta = j['metadata']
        self.title = meta['title']
        abstract = j['abstract']
        self.abstract = abstract if (abstract!=[]) else None
        for paragraph in j['body_text']:
            

    def __str__(self):
        return f'<{self.title}>'


# class Database(object):
    # def __init__(self):
