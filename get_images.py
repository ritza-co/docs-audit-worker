from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def get_html(url):
    try:
      r = requests.get(url)
      print(f"Submitted url is {url}")
      print(f"The redirects list is {r.history}")
    except Exception as e:
      print(e)
      return None

    if url != r.url:
      return {'url': r.url, 'content': r.content}
    else:
      return {'url': url, 'content': r.content}

def get_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.find_all('img')
    try:
      urls = [img['src'] for img in image_tags]
    except Exception as e:
      urls = None
      print(e)
    return urls

def get_absolute_urls(submitted_url, urls):
    absolutes = []
    for url in urls:
        if "#" in url:
            url = url.split("#")[0]
        absolute = urljoin(submitted_url, url)
        if 'base64' not in absolute:
          absolutes.append(absolute)
    return absolutes

def get_images_from_url(url):
    html = get_html(url)
    if type(html) == type(None):
      return None
    else:
      urls = get_urls(html['content'])
    #base_url = '/'.join(html['url'].split("/")[:3])

    if type(urls) == type([]):
      absolutes = get_absolute_urls(html['url'], urls)
      print(f"We found {len(list(set(absolutes)))} images")
      return list(set(absolutes))
    else:
      return None