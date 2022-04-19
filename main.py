from datetime import date
from dateutil.relativedelta import relativedelta

from RPA.Browser.Selenium import Selenium

from nyt_article_search import NYTArticleSearcher

# TODO: put to Robocorp Cloud
phrase = "Ukraine"
category = "Arts"
months = 1

searcher = NYTArticleSearcher()
searcher.start_new_search(phrase)
searcher.apply_category_filter(category)
searcher.apply_date_filter(from_date=date.today() - relativedelta(months=months), to_date=date.today())