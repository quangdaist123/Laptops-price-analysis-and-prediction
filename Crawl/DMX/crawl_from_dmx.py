import json
import jsonlines
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class DienMayXanhScraper:
    """
    Parse comments and ratings of Iphones on
    https://www.dienmayxanh.com/dien-thoai-apple-iphone
    """

    def __init__(self):
        self.driver = self._load_driver()
        self.driver.get("https://www.dienmayxanh.com/laptop/")
        try:
            while True:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "view-more")))
                self.driver.find_element_by_class_name("view-more").click()
        except:
            self.laptops = self.driver.find_elements_by_xpath('//*[@id="categoryPage"]/div[3]/ul/li/a[1]')

    @staticmethod
    def _load_driver():
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        _chrome_options = ChromeOptions()
        _chrome_options.add_argument(f"user-agent={user_agent}")
        # _chrome_options.add_argument("--headless")
        _chrome_options.add_argument("--disable-extensions")
        _chrome_options.add_argument("--incognito")
        _chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=_chrome_options, executable_path="Crawl/DMX/utils/chromedriver_dai.exe")
        return driver

    def _go_to_first_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])

    def _go_to_new_tab(self, *args, link=None) -> None:
        self.driver.execute_script(f'''window.open("{link}","new_window");''')
        self.driver.switch_to.window(self.driver.window_handles[1])

    @staticmethod
    def _append_jsonl_file(data: dict) -> None:
        with open("results.jsonl", "a+", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    @staticmethod
    def _log_errors(data: str) -> None:
        with open("log.txt", "a+", encoding="utf8") as f:
            f.write(data)
            f.write("\n")

    def parse(self, *args, export=False) -> None:
        for i, phone in enumerate(self.laptops):
            print(f"Crawling {i + 1}/{len(self.laptops)}...")
            link = phone.get_attribute("href")
            self._go_to_new_tab(link=link)
            try:
                result = {}
                name = self.driver.find_element_by_css_selector(".detail > h1").text
                price = self.driver.find_element_by_class_name("box-price-present").text
                result["Tên"] = name
                result["Giá"] = price

                self.driver.find_element_by_class_name("btn-short-spec").click()
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "parameter-all"))
                )
                specs = self.driver.find_element_by_class_name("parameter-all").find_elements_by_tag_name("li")
                for spec in specs:
                    name = spec.find_element_by_class_name("ctLeft").text[:-1]
                    info = spec.find_element_by_class_name("ctRight").text
                    result[name] = info
                self._append_jsonl_file(result) if export else print(result)
            except NoSuchElementException or TimeoutException:
                print("Sản phẫm lỗi")
                self._log_errors(link)

            self._go_to_first_tab()
        self.driver.quit()


# %%
bot = DienMayXanhScraper()
bot.parse(export=True)

# %%
data = []
with jsonlines.open("Crawl/DMX/raw/results.jsonl", "r") as f:
    for line in f:
        data.append(line)

#%%
max_num_specs = 0
specifications = []
for line in data:
    if max_num_specs < len(line.keys()):
        max_num_specs = len(line.keys())
        specifications = list(line.keys())

df = pd.DataFrame(columns=specifications)
#%%
for line in data:
    line_filtered = {}
    for spec in specifications:
        if spec not in line.keys():
            line_filtered[spec] = None
        else:
            line_filtered[spec] = line[spec]
    df = df.append(line_filtered, ignore_index=True)

