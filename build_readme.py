import feedparser
import httpx
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse("https://www.havef.fun/blog/rss.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": " ".join(entry["published"].split()[:4]),
        }
        for entry in entries
    ]

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    entries = fetch_blog_entries()[:8]
    entries_md = "\n\n".join(
        ["[{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)
