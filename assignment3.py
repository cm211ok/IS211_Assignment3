import argparse
import csv
import re
import requests

def download_log_file(url):
    """Download the log file from the URL."""
    response = requests.get(url)
    response.raise_for_status()  
    return response.text

def process_log_data(log_data):
    """Process the log data to gather statistics."""
    image_count = 0
    total_requests = 0
    browser_count = {"Firefox": 0, "Chrome": 0, "Internet Explorer": 0, "Safari": 0}
    hour_hits = {str(i).zfill(2): 0 for i in range(24)}  

    image_regex = r'\.(jpg|gif|png)$'
    browsers = {
        "Firefox": r'Firefox',
        "Chrome": r'Chrome',
        "Internet Explorer": r'(MSIE)',
        "Safari": r'Safari'
    }

 
    csv_reader = csv.reader(log_data.splitlines())

    for row in csv_reader:
        if len(row) < 5:
            continue  
        file_path = row[0]
        datetime = row[1]
        user_agent = row[2]
        status_code = row[3]
        
        total_requests += 1

        if re.search(image_regex, file_path):
            image_count += 1

        
        for browser, regex in browsers.items():
            if re.search(regex, user_agent):
                browser_count[browser] += 1
                break  
        
        hour = datetime.split()[1].split(":")[0]
        hour_hits[hour] += 1

    image_percentage = (image_count / total_requests) * 100 if total_requests > 0 else 0
    print(f"Image requests account for {image_percentage:.1f}% of all requests")
    
    most_popular_browser = max(browser_count, key=browser_count.get)
    print(f"The most popular browser is {most_popular_browser}")
    
    sorted_hour_hits = sorted(hour_hits.items(), key=lambda x: x[1], reverse=True)
    for hour, hits in sorted_hour_hits:
        print(f"Hour {hour} has {hits} hits")

def main(url):
    print(f"Running main with URL = {url}...")
    log_data = download_log_file(url)
    process_log_data(log_data)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
