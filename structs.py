class Article(object):
    def __init__(self, id, authors, title, text):
        self.id = id
        self.authors = authors
        self.title = title
        self.text = text

    def __str__(self):
        return f'<{self.title} by {self.authors}>'

    def author_str(self):
        ''' Gets string of authors '''
        
