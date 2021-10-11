import time
from selenium import webdriver
import json
import jsonlines
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class DienMayXanhScraper:
    """
    Parse comments and ratings of Iphones on
    https://www.dienmayxanh.com/dien-thoai-apple-iphone
    """

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver_dai.exe")
        # self.driver.get("https://www.dienmayxanh.com/dien-thoai-apple-iphone/")
        self.driver.get("https://www.dienmayxanh.com/laptop/")
        try:
            while True:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "view-more"))
                )
                self.driver.find_element_by_class_name("view-more").click()
        except ElementNotInteractableException:
            self.laptops = self.driver.find_elements_by_xpath('//*[@id="categoryPage"]/div[3]/ul/li/a[1]')

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
        for phone in self.laptops:
            link = phone.get_attribute("href")
            self._go_to_new_tab(link=link)
            try:
                result = {}
                price = self.driver.find_element_by_class_name("box-price-present").text
                result["Giá"] = price

                self.driver.find_element_by_class_name("btn-short-spec").click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "parameter-all"))
                )
                specs = self.driver.find_element_by_class_name("parameter-all").find_elements_by_tag_name("li")
                for spec in specs:
                    name = spec.find_element_by_class_name("ctLeft").text[:-1]
                    info = spec.find_element_by_class_name("ctRight").text
                    result[name] = info
                    # result = {"text": text, "rating": rating}
                self._append_jsonl_file(result) if export else print(result)
            except NoSuchElementException:
                print("Sản phẫm lỗi")
                self._log_errors(link)

            self._go_to_first_tab()
        self.driver.quit()


# %%
bot = DienMayXanhScraper().parse(export=True)

#%%
specifications = ["Giá",
                  "Thương hiệu",
                  "Cửa hàng",
                  "Công nghệ CPU",
                  "Số nhân",
                  "Tốc độ CPU",
                  "RAM",
                  "Loại RAM",
                  "Hỗ trợ RAM tối đa",
                  "Ổ cứng",
                  "Độ phân giải",
                  "Tần số quét",
                  "Công nghệ màn hình",
                  "Card màn hình",
                  "Webcam",
                  "Đèn bàn phím",
                  "Kích thước, trọng lượng",
                  "Chất liệu",
                  "Thông tin Pin",
                  "Thời điểm ra mắt"]

df = pd.DataFrame(columns=specifications)

with jsonlines.open("results.jsonl", "r") as f:
    for line in f:
        print(line)


line_filtered = {}
for spec in specifications:
    if spec not in line.keys():
        line_filtered[spec] = None
    else:
        line_filtered[spec] = line[spec]
df.append(line_filtered, ignore_index=True)