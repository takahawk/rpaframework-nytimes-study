from RPA.Browser.Selenium import Selenium


class NYTArticleSearcher:
    def start_new_search(self, phrase):
        self.lib = Selenium()

        self.lib.open_available_browser("https://www.nytimes.com/")

        self.lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/button")
        self.lib.input_text("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/div/input", phrase)
        self.lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/button")

    def apply_category_filter(self, filter):
        self._apply_filter(filter,
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/button",
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul")
        self._apply_filter(filter,
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[3]/div/div/button",
                           "//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[3]/div/div/div/ul")

    def apply_date_filter(self, from_date, to_date):
        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button")
        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button")
        self.lib.input_text("startDate", "{:02d}/{:02d}/{}".format(from_date.month, from_date.day, from_date.year))
        self.lib.input_text("endDate", "{:02d}/{:02d}/{}".format(to_date.month, to_date.day, to_date.year))
        self.lib.click_element("//html/body/div[1]/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button")

    def _apply_filter(self, filter, picker_xpath, list_xpath):
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
