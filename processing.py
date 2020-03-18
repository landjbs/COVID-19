'''
File processing to load database
'''


import os


file_folders = ['bioxiv_medrxiv', 'comm_use_subset',
                'noncomm_use_subset', 'pmc_custom_license']



for top_folder in os.listdir('2020-03-13'):
    if top_folder in file_folders:
        for article in os.listdir(f'2020-03-13/{top_folder}/{top_folder}'):
            if not article.endswith('.json'):
                print(article)
