from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def get_html(url):
    r = requests.get(url)
    return r.content

def get_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll("a", href=True)
    return [link["href"] for link in links]

def get_absolute_urls(base_url, submitted_url, urls):
    absolutes = []
    for url in urls:
        print(f"Looping {url}")
        # check if link isn't blank and not a ref to another section on the same page  
        if url and url[0] != '#':
            if "#" in url:
              url = url.split("#")[0]
            absolute = urljoin(submitted_url, url)
            absolutes.append(absolute)
    return absolutes

def get_links_from_url(url):
    html = get_html(url)
    urls = get_urls(html)
    base_url = '/'.join(url.split("/")[:3])
    absolutes = get_absolute_urls(base_url, url, urls)
    return list(set(absolutes))