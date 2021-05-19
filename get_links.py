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
        if "#" in url:
          url = url.split("#")[0]
        if url[0:2] == './':
          relative_base_url = '/'.join(submitted_url.split('/')[:-1])
          absolute = urljoin(relative_base_url, url)
        else:
          print(f"url is {url}")
          absolute = urljoin(base_url, url)
          print(f"absolute is {absolute}")

        absolutes.append(absolute)
    return absolutes

def get_links_from_url(url):
    html = get_html(url)
    urls = get_urls(html)
    base_url = '/'.join(url.split("/")[:3])
    absolutes = get_absolute_urls(base_url, url, urls)
    return list(set(absolutes))