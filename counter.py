"""
Quick and dirty view count scraper
"""
import csv
import re

from bs4 import BeautifulSoup
import requests

YOUTUBE_URLS = ["https://www.youtube.com/watch?v=pZy8115sNXM"]
FACEBOOK_URLS = ["https://www.facebook.com/deccannews/videos/10153799110537160"]

def youtube_count(url):
    """
    Counts the number of views on a Youtube video.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find("div", {"class": "watch-view-count"})
    return content.text

def facebook_count(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # print soup.prettify().encode("UTF-8")
    regex = re.compile("[\d|,]+ Views")
    return regex.findall(page.content)[0]

def dump_to_csv(counts):
    with open("counts.csv", "wb") as csvfile:
        fieldnames = ["url", "count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for count in counts:
            writer.writerow(count)

def main():
    counts = []
    for url in YOUTUBE_URLS:
        count = youtube_count(url)
        counts.append({"url": url, "count": count})
    for url in FACEBOOK_URLS:
        count = facebook_count(url)
        counts.append({"url": url, "count": count})
    dump_to_csv(counts)

if __name__ == "__main__":
    main()
