import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

URL = "https://mpob.gov.my/news/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
STORAGE_FILE = "last_news.json"


def get_latest_news():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []
    rows = table.find_all("tr")[1:]
    news_list = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 3:
            link_tag = cells[1].find("a")
            link = link_tag["href"] if link_tag else None
            news_list.append(
                {
                    "date": cells[0].text.strip(),
                    "title": cells[1].text.strip(),
                    "source": cells[2].text.strip(),
                    "link": link,
                }
            )
    return news_list


def load_last_news():
    if not Path(STORAGE_FILE).exists():
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last_news(news_list):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)


def is_new_news(news_item, saved_news_list):
    return all(item["title"] != news_item["title"] for item in saved_news_list)
