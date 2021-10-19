from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scrape import convert
from Scrape.base_class import BaseScraper


class FPTScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.driver.get("https://fptshop.com.vn/may-doi-tra/may-tinh-xach-tay-cu-gia-re")
        try:
            while True:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cdt-product--loadmore")))
                self.driver.find_element_by_class_name("cdt-product--loadmore").click()
        except:
            self.laptops = self.driver.find_elements_by_css_selector(".mc-lprow>.mc-lpcol")

    def _parse_specs_info(self, product_name):
        specs_info = {}

        # Search google with laptop's name plus "FPT" keyword
        self._go_to_new_tab(link="https://google.com")
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "q")))
            search = self.driver.find_element_by_name("q")
            search.send_keys(product_name + " FPT")
            search.send_keys(Keys.RETURN)
            self.driver.implicitly_wait("5")
            first_result = self.driver.find_element_by_xpath(
                '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]').find_element_by_tag_name("a")
            first_result.click()

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Xem cấu hình chi tiết")))
            self.driver.find_element_by_link_text("Xem cấu hình chi tiết").click()

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.c-modal__content > div.c-modal__row > table.st-table td")))
            list_specs = self.driver.find_elements_by_css_selector(
                "div.c-modal__content > div.c-modal__row > table.st-table td")
            for i in range(0, len(list_specs) - 1, 2):
                specs_info[list_specs[i].text] = list_specs[i + 1].text

            table_specs = self.driver.find_elements_by_css_selector("ul.st-list > li")
            for info in table_specs:
                key, value = info.text.split(":  \n")
                specs_info[key] = value
        except:
            print("Không trích được cấu hình chi tiết")
        finally:
            self.driver.close()
            self._go_to_first_tab()
        return specs_info

    def _parse_every_used_laptop(self, sub_products, base_info):
        results = []
        for product in sub_products:
            try:
                self._go_to_new_tab(link=product.find_element_by_tag_name("a").get_attribute("href"))
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "mc-ctpri1")))
                result = {"Giá đã qua sử dụng": self.driver.find_element_by_class_name("mc-ctpri1").text,
                          "Hạn bảo hành": self.driver.find_element_by_css_selector(".mc-ctttm li:nth-of-type(2)").text}
                result.update(base_info)
                results.append(result)
                self.driver.close()
                self._go_to_last_tab()
            except BaseException as e:
                print(e)
                results.append(base_info["Tên"])
        self.driver.close()
        self._go_to_first_tab()
        return results

    def parse(self, *args, export=False) -> None:
        for laptop in self.laptops:
            try:
                base_info = {"Tên": laptop.find_element_by_class_name("mc-lpiname").text,
                             "Giá mới": laptop.find_element_by_class_name("mc-lpri1").text}

                base_info.update(self._parse_specs_info(base_info["Tên"]))
                self._go_to_new_tab(link=laptop.find_element_by_tag_name("a").get_attribute("href"))
                sub_products = self.driver.find_elements_by_css_selector(".mc-lprow>.mc-lpcol")

                results = self._parse_every_used_laptop(sub_products, base_info)
                for result in results:
                    if isinstance(result, dict):
                        self._append_jsonl_file("FPT_used.jsonl", result)
                    elif isinstance(result, str):
                        self._log_errors("FPT_used_log.txt", result)
            except BaseException as e:
                raise (e)
                print("Lỗi sản phẩm")

# %%
bot = FPTScraper()
bot.parse(export=True)

# %%

raw_data = convert.read_results("Scrape/DMX_new/log/DMX_new.jsonl")
max_columns = convert.get_spec_fields(raw_data)
df = convert.make_frame(raw_data, max_columns)
df.to_csv("raw_data_DMX_new.csv", index=False)
