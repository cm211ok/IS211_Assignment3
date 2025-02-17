import argparse
import csv
import re
from collections import Counter
from urllib.request import urlopen

def download_file(url):
    response = urlopen(url)
    return response.read().decode()

def process_log_data(log_data):
    image_hits = 0
    total_hits = 0
    browser_counts = Counter()
    hourly_hits = [0] * 24 

    image_re = re.compile(r'.*\.(jpg|gif|png)$', re.IGNORECASE)
    browser_re = re.compile(r'(Firefox|Chrome|MSIE|Safari)')

    for line in csv.reader(log_data.splitlines()):
        if not line:
            continue
        file_path, datetime, user_agent, status, _ = line
        total_hits += 1
        
        if image_re.match(file_path):
            image_hits += 1
                browser_match = browser_re.search(user_agent)
        if browser_match:
            browser_counts[browser_match.group(1)] += 1
        
        hour = int(datetime.split()[1].split(':')[0])
        hourly_hits[hour] += 1

    return image_hits, total_hits, browser_counts, hourly_hits

def print_image_stats(image_hits, total_hits):
    image_percentage = (image_hits / total_hits) * 100
    print(f"Image requests account for {image_percentage:.1f}% of all requests")
    print(f"Total image hits: {image_hits}")
    print(f"Total requests: {total_hits}")

def print_most_popular_browser(browser_counts):
    popular_browser = browser_counts.most_common(1)[0][0] if browser_counts else "Unknown"
    print(f"The most popular browser is: {popular_browser}")

def print_hourly_hits(hourly_hits):
    print("Hits by Hour:")
    for hour, count in enumerate(hourly_hits):
        print(f"Hour {hour:02d} has {count} hits")

def main(url):
    print(f"Downloading file from {url}...")
    log_data = download_file(url)
    print("Processing log data...")

    image_hits, total_hits, browser_counts, hourly_hits = process_log_data(log_data)

    print_image_stats(image_hits, total_hits)

    print_most_popular_browser(browser_counts)

    print_hourly_hits(hourly_hits)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process web log file")
    parser.add_argument("--url", help="URL to the web log file", required=True)
    args = parser.parse_args()
    main(args.url)
