from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def get_html(url):
    try:
      r = requests.get(url)
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
    links = soup.findAll("a", href=True)
    try:
      return [link["href"] for link in links]
    except Exception as e:
      print(e)
      return None

def check_valid_links(url):
    if 'tel:' in url:
      print("Skipping tel link")
      return False
    elif 'mailto:' in url:
      print("Skipping mailto link")
      return False
    elif 'localhost:' in url:
      print("Skipping localhost link")
      return False
    else:
      return True

def remove_trailing_slash(absolutes):
    absolutes_with_no_trailing_slash = []
    for absolute in absolutes:
        if absolute[-1] == '/':
            absolute = absolute[:-1]
            absolutes_with_no_trailing_slash.append(absolute)
        else:
            absolutes_with_no_trailing_slash.append(absolute)
    return absolutes_with_no_trailing_slash

def get_absolute_urls(submitted_url, urls):
    absolutes = []
    for url in urls:
        print(f"Looping {url}")
        if check_valid_links(url):
          # check if link isn't blank and not a ref to another section on the same page  
          if url and url[0] != '#':
              if "#" in url:
                url = url.split("#")[0]
              absolute = urljoin(submitted_url, url)
              print(f"Absolute is {absolute}")
              absolutes.append(absolute)
    absolutes_with_no_trailing_slash = remove_trailing_slash(absolutes)
    return absolutes_with_no_trailing_slash

def get_links_from_url(url):
    html = get_html(url)
    if type(html) == type(None):
      return None
    else:
      urls = get_urls(html['content'])
    #base_url = '/'.join(url.split("/")[:3])

    if type(urls) == type([]):
      absolutes = get_absolute_urls(html['url'], urls)
      return list(set(absolutes))
    else:
      return None