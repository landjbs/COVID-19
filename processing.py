'''
File processing to load database
'''


import os
import json
from tqdm import tqdm

from structs import Article, Database
from cleaning import *


tokens = ['co-infection']
knowledgeSet = {clean_text(s) for s in tokens}
knowledgeProcessor = KeywordProcessor(case_sensitive=False)
for i, keyword in enumerate(knowledgeSet):
    knowledgeProcessor.add_keyword(keyword)


database = Database(knowledgeProcessor)
