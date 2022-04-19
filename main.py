from datetime import date
from dateutil.relativedelta import relativedelta

from nyt_article_search import NYTArticleSearcher

# TODO: put to Robocorp Cloud
phrase = "Ukraine"
category = "Arts"
months = 1

searcher = NYTArticleSearcher()
searcher.is_started = True
searcher.start_new_search(phrase)
searcher.apply_category_filter(category)
# TODO: fix date calculation
searcher.apply_date_filter(from_date=date.today() - relativedelta(months=months), to_date=date.today())
searcher.export_articles_to_excel(phrase, download_images=True)