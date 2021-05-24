import requests
import re

def get_image_size(imageUrl):
    print(f"image url is {imageUrl}")
    response = requests.get(imageUrl)
    image_size = len(response.content)
    return image_size

def process_image_urls(urls, site_url):
    oversize_images = []
    right_size_images = []
    all_images = []
    base_url = '/'.join(site_url.split("/")[:3])
    for i, url in enumerate(urls):
      print(f"Determining size for image {i+1}/{len(urls)}")
      print(url)
      filename = re.search(r'/([\w_-]+[.](jpg|jpeg|svg|gif|png))$', url)
      
      if not filename:
          print("Expression didn't match with the url: {}".format(url))
          continue
      if 'http' not in url:
          # add site url to image path if relative
          url = '{}{}'.format(base_url, url)
      print(f"New url is {url}")
      image_size = get_image_size(url)
      print(f"image size of {image_size}")
        
      # check if image is oversize
      if image_size > 100000:
        oversize_images.append({'path': url, 'size': round(image_size/1000)})
        print(f"Image {i+1} has a size of {image_size/1000}KB")
      else:
        right_size_images.append({'path': url, 'size': round(image_size/1000)})

    all_images.append(oversize_images)
    all_images.append(right_size_images)
      
    return all_images

def run_image_audit(images, url):
    all_images = process_image_urls(images, url)
    return all_images