import re

money_amount_pattern = re.compile("(\$\d+\.\d+|\$\d+,\d+\.\d+|\d+\s+dollars|\d+\s+USD)")


class Article:
    def __init__(self, title, date, description, picture, phrase_count):
        self.title = title
        self.date = date
        self.description = description
        self.picture = picture
        self.phrases_count = phrase_count
        self.contains_amount = bool(money_amount_pattern.search(title) or money_amount_pattern.search(description))

    def __str__(self):
        return "Title: {}\nDate: {}\nDescription: {}\nPicture: {}\n"\
               "Phrases Count: {}\nContains money amount: {}\n".format(self.title, self.date,
                                                                         self.description, self.picture,
                                                                         self.phrases_count, self.contains_amount)