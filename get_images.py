from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def get_html(url):
    r = requests.get(url)
    return r.content

def get_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.find_all('img')
    urls = [img['src'] for img in image_tags]
    return urls

def get_absolute_urls(base_url, urls):
    absolutes = []
    for url in urls:
        if "#" in url:
            url = url.split("#")[0]
        absolute = urljoin(base_url, url)
        absolutes.append(absolute)
    return absolutes

def get_images_from_url(url):
    html = get_html(url)
    urls = get_urls(html)
    base_url = '/'.join(url.split("/")[:3])
    absolutes = get_absolute_urls(base_url, urls)
    print(f"We found {len(list(set(absolutes)))} images")
    return list(set(absolutes))