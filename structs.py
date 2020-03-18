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


# class Database(object):
    # def __init__(self):
