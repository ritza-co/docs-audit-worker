import requests

def check_broken_links(absolutes):
    broken_links = []
    working_links = []
    all_links = []
    for i, absolute in enumerate(absolutes):
        print(absolute)
        print(f"processing {i+1}/{len(absolutes)}")
        try:
            r = requests.get(absolute)
        except:
            print(f"Failed to get the link {absolute}")
        if not r.ok:
            broken_links.append({'link': absolute, 'code': r.status_code})
            print(absolute)
            print(f"failed with status {r.status_code}")
        else:
            working_links.append(absolute)
            print("OK")
    all_links.append(broken_links)
    all_links.append(working_links)
    return all_links

def run_link_audit(links):
    print(f"Found {len(links)} urls - auditing")
    audited_links = check_broken_links(links)

    return audited_links