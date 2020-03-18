import os
import json
from tqdm import tqdm

from cleaning import clean_text, clean_title
import processing as find_raw_tokens

class Article(object):
    def __init__(self, j, tokenizer):
        # get metadata
        self.id = j['paper_id']
        meta = j['metadata']
        self.title = clean_title(meta['title'])
        # cache text and process tokens
        tokens = {}
        self.abstract = []
        for paragraph in j['abstract']:
            text = clean_text(paragraph['text'])
            para_tokens = tokenizer.
            self.abstract.append()
        self.paragraphs = []
        for paragraph in j['body_text']:
            self.paragraphs.append(clean_text(paragraph['text']))

    def __str__(self):
        return f'<{self.title}>'

    def display(self):
        print(self.title)
        print('\n'.join(self.paragraphs))



class Database(object):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        x = [i for i in self.process_articles()]

    def process_articles(self):
        tokenizer = self.tokenizer
        file_folders = ['bioxiv_medrxiv', 'comm_use_subset',
                        'noncomm_use_subset', 'pmc_custom_license']
        for top_folder in tqdm(os.listdir('2020-03-13')):
            if top_folder in file_folders:
                for path in os.listdir(f'2020-03-13/{top_folder}/{top_folder}'):
                    if path.endswith('.json'):
                        path = f'2020-03-13/{top_folder}/{top_folder}/{path}'
                        with open(path, 'r') as load_file:
                            article_json = json.load(load_file)
                            article_obj = Article(article_json, tokenizer)
                            yield article_obj
