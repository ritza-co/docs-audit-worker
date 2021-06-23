import os
import requests
import time
from image_audit import run_image_audit
from link_audit import run_link_audit
from get_links import get_links_from_url
from get_images import get_images_from_url

GET_WORK_URL = "https://docs-audit-server.ritza.repl.co/task-request"
SUBMIT_WORK_URL = "https://docs-audit-server.ritza.repl.co/result"

WORKER_ID = os.getenv("REPL_OWNER") + "_" + os.getenv("REPL_SLUG")

def get_task():
    jsn = {"worker_id": WORKER_ID}
    r = requests.post(GET_WORK_URL, json=jsn)
    print(r)
    try:
        return r.json()
    except Exception as e:
        print("Couldn't get JSON")
        print(e)
        try:
            print(r.content)
        except:
            print("Couldn't print content")

def do_work(task):
    if task['task_type'] == "link_audit":
        url = task['input_data']
        links = get_links_from_url(url)

        if type(links) == type(None):
          print("Couldn't get links. Aborting link audit task")
          task_results = None
        else:
          print("Got links, starting link audit now")
          links_audit = run_link_audit(links)

          task_results = {'total_links': len(links), 'all_links': links_audit}

    elif task['task_type'] == "image_audit":
        print("Starting image audit task")
        url = task['input_data']
        images = get_images_from_url(url)

        if type(images) == type(None):
          print("Couldn't get images. Aborting image audit task")
          task_results = None
        else:
          all_images = run_image_audit(images, url)

          task_results = {'image_count': len(images), 'oversize_images': all_images[0], 'right_size_images': all_images[1], 'broken_images': all_images[2], 'broken_status_codes': all_images[3]}

    return task_results

def submit_results(task_id, task_type, task_url, first_task, output):
    jsn = {
        "worker_id": WORKER_ID,
        "task_id": task_id,
        "task_url": task_url,
        "task_type": task_type,
        "first_task": first_task,
        "output": output,
    }
    r = requests.post(SUBMIT_WORK_URL, json=jsn)

def main():
    while True:
        print("getting new task")
        task = get_task()
        if not task:
            print("No new task. Sleeping for 60 seconds")
            time.sleep(60)
        elif task:
            print("Got task, starting work")
            output = do_work(task)
            print("submitting")
            submit_results(task['task_id'], task['task_type'], task['input_data'], task['first_task'], output)
            print("done")

if __name__ == "__main__":
    main()