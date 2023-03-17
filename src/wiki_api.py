import requests
from bs4 import BeautifulSoup
import Levenshtein
import wikipediaapi
import wikipedia
import re
import numpy as np

wiki_wiki = wikipediaapi.Wikipedia('en')

def get_sentence_num(offset, full_stops):
    if not len(full_stops): return 0
    return np.argmax(offset<full_stops) if offset<full_stops[-1] else len(full_stops)

def get_linked_article(link):
    url = link['href']
    url = url.replace("/wiki/", "").replace("_", " ")
    return url

def finalize_link_info(offset, link, paragraph):
    parent_text = link.parent.get_text()
    link_text = link.get_text()
    link_pos = offset+parent_text.find(link_text)
    full_stops = np.array([m.start() for m in re.finditer('\.', parent_text)])
    return (link_pos, get_linked_article(link), paragraph, get_sentence_num(link_pos, full_stops))

cached_links = {}
async def get_summary_links(session, title):
    if title in cached_links: return title, cached_links[title]

    url = "https://en.wikipedia.org/wiki/" + str(title).replace(" ", "_")
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        
        for elem in soup.find_all(class_='mw-indicators'): # for good articles
            elem.decompose()

        summ = soup.find(class_='mw-parser-output') # Find the element or elements that contain the summary

        # cleaning of thumbnails, shortdescriptions, hatnotes and style tags
        to_clean_divs = summ.find_all('div', class_='thumb tright') + summ.find_all('div', class_='shortdescription') + summ.find_all('div', class_='hatnote') + summ.find_all('style') + summ.find_all('link') + summ.find_all('table', class_='metadata') + summ.find_all('a', class_='selflink')
        for div in to_clean_divs:
            div.decompose()

        if soup.find('table', class_=re.compile(r'infobox.*biography')):
            #print("person detected on " + url)
            return title, None

        cutoff_div = summ.find(id='toc') # Find the div element with the id "toc"
        
        if cutoff_div is None:
            cutoff_div = summ.find('h2')
            if cutoff_div is None:
                #print(" unexpected page content on "+ url)
                return title, None

        if 'toc' in cutoff_div.parent.get('class')[0]: cutoff_div = cutoff_div.parent
        preceding_elements = cutoff_div.find_previous_siblings()

        links = []
        offset = 0

        for paragraph, element in enumerate(reversed(preceding_elements)):
            text = element.get_text()
            element_links = element.find_all('a', recursive=False)
            links.extend([(offset, link, paragraph) for link in element_links])
            offset += len(text)

        result = [finalize_link_info(offset, link, paragraph)  for (offset, link, paragraph) in links]
        cached_links[title] = result
        return title, result

def get_first_paragraph(title):
    url = "https://en.wikipedia.org/wiki/" + str(title).replace(" ", "_")
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    for elem in soup.find_all(class_='mw-indicators'): # for good articles
        elem.decompose()

    summ = soup.find(class_='mw-parser-output') # Find the element or elements that contain the summary

    # cleaning of thumbnails, shortdescriptions, hatnotes and style tags
    to_clean_divs = summ.find_all('div', class_='thumb tright') + summ.find_all('div', class_='shortdescription') + summ.find_all('div', class_='hatnote') + summ.find_all('style') + summ.find_all('link') + summ.find_all('table', class_='metadata')
    for div in to_clean_divs:
        div.decompose()

    cutoff_div = summ.find(id='toc') # Find the div element with the id "toc"
    if cutoff_div is None:
        cutoff_div = summ.find('h2')
        if cutoff_div is None:
            print(" unexpected page content on "+ url)
            return None
   
    if 'toc' in cutoff_div.parent.get('class')[0]: cutoff_div = cutoff_div.parent
    preceding_elements = cutoff_div.find_previous_siblings()
    
    return list(reversed(preceding_elements))[0].text

## helper functions for disambiguation
def get_page(title):
    try:
        page = wiki_wiki.page(title)
        return page
    except wikipediaapi.exceptions.DisambiguationError:
        print("Could not disambiguate: " + title)
    except wikipediaapi.exceptions.PageError:
        print("Could not find page: " + title)
    except TimeoutError:
        print("Time out on " + title)
        return get_page(title)
    return None

def is_disambiguation(page):
    return page.summary[0:50].find("refer") != -1

def accept_search_result(search_result, link_set):
    page = get_page(search_result)
    # filter disambiguation pages
    if is_disambiguation(page): return False
    # have at least one outgoing link to a page of the link set
    if not link_set: return True
    return len(link_set.intersection(page.links)) > 0

def strip_parenthesis(title):
    return re.sub(r'\([^)]*\)', '', title).strip()

def disambiguate(term, link_set, field=None):
    field_suffix = "" if field is None else f" ({field})"
    search_results = wikipedia.search(f"{term}{field_suffix}")
    search_results_wo_suffix = list(map(strip_parenthesis, search_results))
    dists = list(map(lambda x: Levenshtein.distance(term, x.lower()), search_results_wo_suffix))
    unsorted_search_results = search_results.copy()
    def get_dist(result): return dists[unsorted_search_results.index(result)]
    search_results.sort(key=get_dist) # sort by Levenshtein distances
    for title in search_results: 
        if accept_search_result(title, link_set): return title
    return None

