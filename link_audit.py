import requests
import time

def check_broken_links(absolutes):
    broken_links = []
    broken_status_codes = []
    working_links = []
    all_links = []
    for i, absolute in enumerate(absolutes):
        print(f"processing {i+1}/{len(absolutes)}")
        try:
            print("getting request", absolute)
            r = requests.get(absolute, timeout=(1, 5))
            print("got request")
            if r.status_code == 429:
                print("429, entering backoff")
                for attempt in [3, 5, 8, 13]:
                    print(f"attempt {attempt} seconds")
                    time.sleep(attempt)
                    re= requests.get(absolute)
                    print("got request")
                    if re.ok:
                      print("re is ok")
                      working_links.append({'link': absolute, 'code': re.status_code})
                      print("OK1")
                      break
                    elif not re.ok and re.status_code != 429:
                      print("re is not 429")
                      broken_status_codes.append({'link': absolute, 'code': re.status_code})
                      print(f"failed1 with status {re.status_code}")
                      break
            elif not r.ok and r.status_code != 429:
                print("r not ok and not 429")
                broken_status_codes.append({'link': absolute, 'code': r.status_code})
                print(absolute)
                print(f"failed with status {r.status_code}")
            elif r.ok:
                print("r is ok")
                working_links.append({'link': absolute, 'code': r.status_code})
                print("OK")
        except Exception as e:
            broken_links.append({'link': absolute, 'code': "Failed to get the link"})
            print(e)
            print(f"Failed to get the link {absolute}")
    print("done returning after appending")
    all_links.append(broken_links)
    all_links.append(working_links)
    all_links.append(broken_status_codes)
    print("append done")
    return all_links

def run_link_audit(links):
    print(f"Found {len(links)} urls - auditing")
    audited_links = check_broken_links(links)

    return audited_links