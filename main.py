from datetime import date
from dateutil.relativedelta import relativedelta
import json

from nyt_article_search import NYTArticleSearcher

# TODO: move to Robocorp Cloud
with open("config.json") as json_config:
    # load config to variables
    locals().update(json.load(json_config))

searcher = NYTArticleSearcher()
searcher.is_started = True
searcher.start_new_search(phrase)
searcher.apply_category_filter(category)
# TODO: fix date calculation
searcher.apply_date_filter(from_date=date.today() - relativedelta(months=months), to_date=date.today())
searcher.export_articles_to_excel(phrase, download_images=True)