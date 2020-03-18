'''
File processing to load database
'''


import os
import json
from tqdm import tqdm
from collections import Counter

from processing.cleaning import clean_text, clean_title

top_path = 'data/in_data/2020-03-13'
file_folders = ['bioxiv_medrxiv', 'comm_use_subset',
                'noncomm_use_subset', 'pmc_custom_license']

# set to hold all tokens
tokens = set()

for top_folder in tqdm(os.listdir(top_path)):
    if top_folder in file_folders:
        for path in os.listdir(f'{top_path}/{top_folder}/{top_folder}'):
            if path.endswith('.json'):
                path = f'{top_path}/{top_folder}/{top_folder}/{path}'
                with open(path, 'r') as load_file:
                    j = json.load(load_file)
                    # get tokens from title
                    for token in clean_title(j['metadata']['title']).split():
                        tokens.add(token)
                    # get tokens from abstract
                    for paragraph in j['abstract']:
                        for token in (clean_text(paragraph['text'])).split():
                            tokens.add(token)
                    # get tokens from body
                    for paragraph in j['body_text']:
                        for token in (clean_text(paragraph['text'])).split():
                            tokens.add(token)
print(len(tokens))
print(tokens)
