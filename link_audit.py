import requests

def check_broken_links(absolutes):
    broken_links = []
    broken_status_codes = []
    working_links = []
    all_links = []
    for i, absolute in enumerate(absolutes):
        print(f"processing {i+1}/{len(absolutes)}")
        try:
            r = requests.get(absolute)
            if not r.ok:
                broken_status_codes.append({'link': absolute, 'code': r.status_code})
                print(absolute)
                print(f"failed with status {r.status_code}")
            else:
                working_links.append({'link': absolute, 'code': r.status_code})
                print("OK")
        except Exception as e:
            broken_links.append({'link': absolute, 'code': "Failed to get the link"})
            print(e)
            print(f"Failed to get the link {absolute}")
    all_links.append(broken_links)
    all_links.append(working_links)
    all_links.append(broken_status_codes)
    return all_links

def run_link_audit(links):
    print(f"Found {len(links)} urls - auditing")
    audited_links = check_broken_links(links)

    return audited_links