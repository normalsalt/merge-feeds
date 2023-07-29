from feedgen.feed import FeedGenerator
import feedparser
import sys

FILENAME = sys.argv[1]


def get_urls():
    with open(f'{FILENAME}.txt', encoding="utf-8") as f:
        urls = list(map(str.strip, f))

    return urls


def merge_entries(urls):
    entries = []
    for url in urls:
        d = feedparser.parse(url)
        entries.extend(d.entries)
    entries.sort(key=lambda e: e.updated_parsed)

    return entries


def merge_feeds(fg, entries):
    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.link(href=entry.link)

    return fg


fg = FeedGenerator()

fg.title('Merged Feed')
fg.link(href=f'https://normalsalt.github.io/merge-feeds/{FILENAME}.xml')
fg.description('This is a merged RSS feed from multiple sources.')

urls = get_urls()
entries = merge_entries(urls)
fg = merge_feeds(fg, entries)

fg.rss_str(pretty=True)
fg.rss_file(f'{FILENAME}.xml')
