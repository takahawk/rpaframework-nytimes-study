from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from SeleniumLibrary.errors import ElementNotFound

from article import Article


class NYTArticleSearcher:
    is_started = False

    def start_new_search(self, phrase):
        self.phrase = phrase
        self.lib = Selenium()
        self.http = HTTP()

        self.lib.open_available_browser("https://www.nytimes.com/")

        self.lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/button")
        self.lib.input_text("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/div/input", phrase)
        self.lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/button")
        self.is_started = True

    def apply_category_filter(self, filter):
        assert self.is_started

        self._apply_filter(filter,
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/button",
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul")
        self._apply_filter(filter,
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[3]/div/div/button",
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[3]/div/div/div/ul")

    def apply_date_filter(self, from_date, to_date):
        assert self.is_started

        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button")
        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button")
        self.lib.input_text("startDate", "{:02d}/{:02d}/{}".format(from_date.month, from_date.day, from_date.year))
        self.lib.input_text("endDate", "{:02d}/{:02d}/{}".format(to_date.month, to_date.day, to_date.year))
        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button")

    def get_articles(self, download_images=False):
        assert self.is_started

        index = 1
        while True:
            try:
                item = self.lib.find_element("//html/body/div[1]/div[2]/main/div/div[2]/div[2]/ol/li[{}]".format(index))
            except ElementNotFound:
                try:
                    # click "show more"
                    self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[2]/div[3]/div/button")
                except ElementNotFound:
                    return
                continue

            index += 1

            try:
                item.find_element_by_xpath(".//div/h3")
                is_advertisement = True
            except:
                is_advertisement = False
            if is_advertisement:
                continue

            # TODO: parse a date
            date = item.find_element_by_xpath(".//div/span").text
            name = item.find_element_by_xpath(".//div/div/div/a/h4").text
            desc = item.find_element_by_xpath(".//div/div/div/a/p").text
            picture = item.find_element_by_xpath(".//div/div/figure/div/img").get_attribute("src")
            if download_images:
                filename = "images/{}".format(picture.rsplit('/', 1)[-1].rsplit('?', 1)[0])
                self.http.download(picture, filename)
                picture = filename
            phrase_count = name.count(self.phrase) + desc.count(self.phrase)
            yield Article(name, date, desc, picture, phrase_count)

    def export_articles_to_excel(self, filename, download_images=False):
        assert self.is_started

        files = Files()
        book = files.create_workbook("{}.xlsx".format(filename))
        # TODO: format?
        book.set_cell_value(1, 1, "Title")
        book.set_cell_value(1, 2, "Date")
        book.set_cell_value(1, 3, "Description")
        book.set_cell_value(1, 4, "Picture filename")
        book.set_cell_value(1, 5, "Count of search phrases")
        book.set_cell_value(1, 6, "Contains amount of money")

        row_index = 2
        for article in self.get_articles(download_images):
            book.set_cell_value(row_index, 1, article.title)
            book.set_cell_value(row_index, 2, article.date)
            book.set_cell_value(row_index, 3, article.description)
            book.set_cell_value(row_index, 4, article.picture)
            book.set_cell_value(row_index, 5, article.phrases_count)
            book.set_cell_value(row_index, 6, article.contains_amount)
            row_index += 1
        book.save("{}.xlsx".format(filename))

    def _apply_filter(self, filter, picker_xpath, list_xpath):
        assert self.is_started

        self.lib.click_element(picker_xpath)
        elem = self.lib.find_element(list_xpath)
        children = elem.find_elements_by_xpath(".//li")
        for child in children:
            try:
                number = child.find_element_by_xpath(".//button/span").text
            except:
                try:
                    number = child.find_element_by_xpath(".//label/span/span").text
                except:
                    number = ""
            name = child.text[:-len(number)]
            if name == filter:
                child.click()
                return
        self.lib.click_element(picker_xpath)
