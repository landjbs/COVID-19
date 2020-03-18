'''
File processing to load database
'''


import os
import json
from tqdm import tqdm
from collections import Counter

from utils import save_pickle
from processing.cleaning import clean_text, clean_title

# dict mapping all ids to article url


print(len(tokens))
print(tokens)

save_pickle(tokens, 'data/out_data/token_set.save')
