'''
File processing to load database
'''


import os
import json
from tqdm import tqdm

from flashtext import KeywordProcessor
from structs import Article, Database
from cleaning import *


tokens = ['co-infection']
knowledgeSet = {clean_text(s) for s in tokens}
tokenizer = KeywordProcessor(case_sensitive=False)
for i, keyword in enumerate(knowledgeSet):
    tokenizer.add_keyword(keyword)


database = Database(tokenizer)
