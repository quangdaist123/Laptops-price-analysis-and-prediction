import os
os.environ["PATH"] += "C:\\Users\\quang\\PycharmProjects\\laptops-price-analysis-and-prediction\\Scrape"

import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from abc import ABC, abstractmethod


class BaseScraper(ABC):

    def __init__(self):
        self.driver = self._load_driver()

    @staticmethod
    def _load_driver():
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/90.0.4430.93 Safari/537.36"
        _chrome_options = ChromeOptions()
        _chrome_options.add_argument(f"user-agent={user_agent}")
        # _chrome_options.add_argument("--headless")
        _chrome_options.add_argument("--disable-extensions")
        _chrome_options.add_argument("--incognito")
        _chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=_chrome_options, executable_path="chromedriver_dai.exe")
        return driver

    def _go_to_first_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])

    def _go_to_new_tab(self, *args, link=None) -> None:
        self.driver.execute_script(f'''window.open("{link}","new_window");''')
        self.driver.switch_to.window(self.driver.window_handles[1])

    @staticmethod
    def _append_jsonl_file(filename: str, data: dict) -> None:
        with open(filename, "a+", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    @staticmethod
    def _log_errors(filename: str, data: str) -> None:
        with open(filename, "a+", encoding="utf8") as f:
            f.write(data)
            f.write("\n")

    @abstractmethod
    def parse(self, *args, export=False) -> None:
        pass
