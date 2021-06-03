import requests
import re

# returns image size and http code
def get_image_size(imageUrl):
    print(f"image url is {imageUrl}")
    image_request_results = {}
    try:
      response = requests.get(imageUrl)
      if not response.ok:
          image_size = 0
          status_code = response.status_code
          image_request_results['image_size'] = image_size
          image_request_results['status_code'] = status_code
      else:
          image_size = len(response.content)
          status_code = response.status_code
          image_request_results['image_size'] = image_size
          image_request_results['status_code'] = status_code
          print("OK")
    except Exception as e:
      print(e)
      image_size = None
      status_code = None
      image_request_results['image_size'] = image_size
      image_request_results['status_code'] = status_code
    return image_request_results

def process_image_urls(urls, site_url):
    oversize_images = []
    right_size_images = []
    broken_images = []
    broken_status_codes = []
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
      image_request_results = get_image_size(url)
      image_size = image_request_results['image_size']
      print(f"image size of {image_size}")
        
      try:
      # check if image is oversize
        if image_size > 100000:
          oversize_images.append({'path': url, 'size': round(image_size/1000), 'code': image_request_results['status_code']})
          print(f"Image {i+1} has a size of {image_size/1000}KB")
        elif image_size == 0:
          broken_status_codes.append({'path': url, 'size': round(image_size/1000), 'code': image_request_results['status_code']})
        else:
          right_size_images.append({'path': url, 'size': round(image_size/1000), 'code': image_request_results['status_code']})
      except Exception as e:
        print(e)
        broken_images.append({'path': url, 'size': None, 'code': image_request_results['status_code']})

    all_images.append(oversize_images)
    all_images.append(right_size_images)
    all_images.append(broken_images)
    all_images.append(broken_status_codes)
      
    return all_images

def run_image_audit(images, url):
    all_images = process_image_urls(images, url)
    return all_images