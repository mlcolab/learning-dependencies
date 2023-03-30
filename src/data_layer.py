# This file provides convenience functions to access data

import os
import pandas as pd
import numpy as np
import pickle
from collections import Counter

def get_smallest_page(pages):
    if not isinstance(pages, float) and "nan" in pages: return None
    pages_int = [int(pages)] if isinstance(pages, float) else list(map(int, pages.split(",")))
    return min(pages_int)

def read_index_and_wiki_concepts(include_counts=False):
    path = "../dat/index_by_wiki/"
    wiki_concepts = []
    indices = {}
    
    for book in os.listdir(path):
        index = pd.read_csv(path + book).dropna()
        index['first_page'] = index.pages.apply(get_smallest_page) # add first page of index entry
        indices[book] = index
        wiki_concepts.extend(index.wiki_concept) # add new concepts to set
    counts = Counter(wiki_concepts)
    wiki_concepts = counts.keys()
    wiki_concepts = np.array(list(wiki_concepts))
    if include_counts: return indices, wiki_concepts, pd.DataFrame({"concept": wiki_concepts, "count": counts.values()})
    return indices, wiki_concepts

def get_mentions_by_offset(book, min_pr=0.001, min_span=4):
    title = book.replace(".csv", "")
    annotations = pickle.load(open("../dat/annotations/" + title + ".pkl", "rb"))
    mentions_by_offset = {}

    for a in annotations:
        for s in a['support']:
            if s['pageRank'] < min_pr: continue
            if s['chTo'] - s['chFrom'] < min_span: continue
            if s['chFrom'] in mentions_by_offset: # if there was already something at this offset
                if s['pageRank'] > mentions_by_offset[s['chFrom']]['pr']: # if this support has a higher PR
                    mentions_by_offset[s['chFrom']] = {'title': a['title'], 'pr': s['pageRank']} # override
            else: # if no mention by this offset
                mentions_by_offset[s['chFrom']] = {'title': a['title'], 'pr': s['pageRank']} # add
    
    return mentions_by_offset, np.array(list(mentions_by_offset.keys()))

page_correction = {
    'Kuttler-LinearAlgebra-AFirstCourse-2017A.csv': 12,
    'Beezer_First_Course.csv': 14,
    'textbook_Hoffman_Kunze.csv': 9,
    'Nicholson-OpenLAWA-2019A.csv': 22,
    'Linear algebra done right — Axler.csv': 16,
    'Math1410_print.csv': 8,
    'Hefferon_LinAlgebra.csv': 10,
    'linear-Cherey, Denton.csv': 0,
    'interactive_textbook.csv': 18,
    'CollegeAlgCoreq-WEB.csv': 10
}

def get_page_offsets():
    full_text = pd.read_json("../dat/parsed_books/parsed_books.json")
    return full_text.pages.apply(lambda pages: np.cumsum(list(map(len, pages))))

def get_first_page_for_concept(index, concept):
    vals = index.first_page.iloc[index.wiki_concept.values==concept].values
    return vals[0] if len(vals) else None