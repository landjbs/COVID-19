'''
File processing to load database
'''


import os
import json
from tqdm import tqdm
from collections import Counter

from utils import save_pickle
from processing.cleaning import clean_text, clean_title
