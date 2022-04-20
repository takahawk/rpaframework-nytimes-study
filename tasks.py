import os
from datetime import date
import json

from nyt_article_search import NYTArticleSearcher

def main():
    searcher = NYTArticleSearcher()
    try:
        # TODO: move to Robocorp Cloud
        with open("config.json") as json_config:
            # load config to variables
            config = json.load(json_config)

        phrase = os.getenv("PHRASE") or config['phrase']
        category = os.getenv("CATEGORY") or config['category']
        months = int(os.getenv("MONTHS") or config['months'])
        if months > 0:
            months -= 1

        searcher.start_new_search(phrase)
        searcher.apply_category_filter(category)
        # TODO: fix date calculation
        today = date.today()
        start_date = date(today.year, today.month - months, 1)

        searcher.apply_date_filter(from_date=start_date, to_date=today)
        searcher.export_articles_to_excel(phrase, download_images=True)
    finally:
        searcher.stop()

if __name__ == "__main__":
    main()