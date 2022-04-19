from RPA.Browser.Selenium import Selenium

# TODO: put to Robocorp Cloud
phrase = "Ukraine"
category = ""
months = 1

lib = Selenium()

lib.open_available_browser("https://www.nytimes.com/")
lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/button")
lib.input_text("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/div/input", phrase)
lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/button")