import pandas as pd
import re
from Scrape.base_class import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scrape import convert


class TGDD_Scraper(BaseScraper):
    def __init__(self):
        super(TGDD_Scraper, self).__init__(driver_type="edge")
        self.driver.get("https://www.thegioididong.com/may-doi-tra/laptop")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dong")))
        self.driver.find_element_by_class_name("dong").click()
        try:
            while True:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btnviewmoresp")))
                self.driver.find_element_by_class_name("btnviewmoresp").click()
        except:
            self.laptops = self.driver.find_elements_by_css_selector('.products > li')

    def _parse_base_info(self, products):
        base_info = {}
        products[0].click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "wrap_content")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "viewparameterfull")))
        self.driver.find_element_by_class_name("viewparameterfull").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".parameterfull > li[class]")))
        specs = self.driver.find_elements_by_css_selector(".parameterfull > li[class]")
        for spec in specs:
            name = spec.find_element_by_tag_name("span").text
            info = spec.find_element_by_tag_name("li>div").text
            base_info[name] = info

        WebDriverWait(self.driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.loading-cart")))
        self.driver.find_element_by_class_name("iconused-closed").click()
        WebDriverWait(self.driver, 10).until_not(EC.element_to_be_clickable((By.CLASS_NAME, "iconused-closed")))
        return base_info

    def _parse_every_used_laptop(self, sub_products, base_info):
        results = []
        for product in sub_products:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".products > li > div.imagebox")))
                product.click()
                result = {}

                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "priceused")))
                result["Giá đã qua sử dụng"] = self.driver.find_element_by_class_name("priceused").text
                result.update(base_info)
                results.append(result)

                WebDriverWait(self.driver, 10).until_not(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.loading-cart")))
                self.driver.find_element_by_class_name("iconused-closed").click()
                WebDriverWait(self.driver, 10).until_not(EC.element_to_be_clickable((By.CLASS_NAME, "iconused-closed")))
            except:
                failed_laptop = product.find_element_by_tag_name("img").get_attribute("alt")
                results.append(failed_laptop)
        return results

    def parse(self, *args, export=False) -> None:
        for laptop in self.laptops:
            try:
                base_info = {}
                base_info["Tên"] = laptop.find_element_by_tag_name("h3").text
                base_info["Giá mới"] = laptop.find_element_by_tag_name("label").text

                self._go_to_new_tab(link=laptop.find_element_by_tag_name("a").get_attribute("href"))
                sub_products = self.driver.find_elements_by_css_selector(".products > li > div.imagebox")

                base_info.update(self._parse_base_info(sub_products))
                results = self._parse_every_used_laptop(sub_products, base_info)
                for result in results:
                    if isinstance(result, dict):
                        self._append_jsonl_file("TGDD_used.jsonl", result)
                    elif isinstance(result, str):
                        self._log_errors("TGDD_used_log.txt", result)
            except:
                print("Lỗi load trang")
            finally:
                self.driver.close()

            self._go_to_first_tab()


bot = TGDD_Scraper()
bot.parse(export=True)

# %%

raw_data = convert.read_results("Scrape/TGDD_used/TGDD_used.jsonl")
max_columns = convert.get_spec_fields(raw_data)
df = convert.make_frame(raw_data, max_columns)
df.to_csv("raw_data_TGDD_all_used.csv", index=False)

# %%

# Lấy trung bình giá cũ của các máy cùng loại
df["Giá đã qua sử dụng"] = df["Giá đã qua sử dụng"].apply(lambda x: int(re.sub("\D", "", x)))
df_group = df.groupby("Tên")["Giá đã qua sử dụng"].mean()
df_group = df_group.astype("int")
df["Giá đã qua sử dụng"] = df.apply(lambda x: df_group[x["Tên"]], axis=1)
df = df.groupby('Tên', as_index=False).first()

df.to_csv("raw_data_TGDD_avg_used.csv", index=False)

# %%

raw_data = convert.read_results("Scrape/TGDD_used/TGDD_used.jsonl")
max_columns = convert.get_spec_fields(raw_data)
df = convert.make_frame(raw_data, max_columns)
df.to_csv("raw_data_TGDD_all_used.csv", index=False)
