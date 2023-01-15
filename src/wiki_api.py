import requests
from bs4 import BeautifulSoup
import re

def get_summary_links(title, only_summary_links=True):
    url = "https://en.wikipedia.org/wiki/" + str(title).replace(" ", "_")
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    for elem in soup.find_all(class_='mw-indicators'): # for good articles
        elem.decompose()

    summ = soup.find(class_='mw-parser-output') # Find the element or elements that contain the summary

    # cleaning of thumbnails, shortdescriptions, hatnotes and style tags
    to_clean_divs = summ.find_all('div', class_='thumb tright') + summ.find_all('div', class_='shortdescription') + summ.find_all('div', class_='hatnote') + summ.find_all('style') + summ.find_all('link') + summ.find_all('table', class_='metadata')
    for div in to_clean_divs:
        div.decompose()

    if soup.find('table', class_=re.compile(r'infobox.*biography')):
        print("person detected on " + url)
        return None

    if only_summary_links:
        cutoff_div = summ.find(id='toc') # Find the div element with the id "toc"
        
        if cutoff_div is None:
            cutoff_div = summ.find('h2')
            if cutoff_div is None:
                print(" unexpected page content on "+ url)
                return None
    
        if 'toc' in cutoff_div.parent.get('class')[0]: cutoff_div = cutoff_div.parent
        preceding_elements = cutoff_div.find_previous_siblings()
    else:
        preceding_elements = summ

    links = []
    offset = 0
    for paragraph, element in enumerate(reversed(preceding_elements)):
        element_links = element.find_all('a', recursive=False)
        links.extend([(offset, link, paragraph) for link in element_links])
        offset += len(element.get_text())

    return [(offset+link.parent.get_text().find(link.get_text()), link.get('title'), paragraph) for (offset, link, paragraph) in links]

cached_links = {}
def get_cached_links(title):
    if title not in cached_links: cached_links[title] = get_summary_links(title)
    return cached_links[title]

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
    
    return reversed(preceding_elements)[0].text