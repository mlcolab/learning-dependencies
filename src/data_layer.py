import os
import pandas as pd
import numpy as np

def get_smallest_page(pages):
    if not isinstance(pages, float) and "nan" in pages: return None
    pages_int = [int(pages)] if isinstance(pages, float) else list(map(int, pages.split(",")))
    return min(pages_int)

def read_index_and_wiki_concepts():
    path = "../dat/index_by_wiki/"
    wiki_concepts = set()
    indices = {}
    for book in os.listdir(path):
        index = pd.read_csv(path + book).dropna()
        index['first_page'] = index.pages.apply(get_smallest_page) # add first page of index entry
        indices[book] = index
        wiki_concepts.update(index.wiki_concept) # add new concepts to set
    wiki_concepts = np.array(list(wiki_concepts))
    
    return indices, wiki_concepts