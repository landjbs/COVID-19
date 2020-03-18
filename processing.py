'''
File processing to load database
'''


import os
import json
from tqdm import tqdm

from structs import Article


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
