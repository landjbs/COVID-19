'''
File processing to load database
'''


import os
import json


file_folders = ['bioxiv_medrxiv', 'comm_use_subset',
                'noncomm_use_subset', 'pmc_custom_license']


def parse_article_json(file):
    


for top_folder in os.listdir('2020-03-13'):
    if top_folder in file_folders:
        for path in os.listdir(f'2020-03-13/{top_folder}/{top_folder}'):
            if path.endswith('.json'):
                path = f'2020-03-13/{top_folder}/{top_folder}/{path}'
                with open(path, 'r') as load_file:
                    article_json = json.load(load_file)
                    print(article_json)
