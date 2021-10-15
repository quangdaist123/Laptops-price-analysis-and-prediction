from Scrape.base_class import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scrape.DMX.utils import convert


class TGDD_Scraper(BaseScraper):
    def __init__(self):
        super(TGDD_Scraper, self).__init__()
        self.driver.get("https://www.thegioididong.com/may-doi-tra/laptop?p=duoi-15-trieu&o=gia-cao-den-thap/")
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
        specs = self.driver.find_elements_by_css_selector(".parameterfull > li[class]")
        for spec in specs:
            name = spec.find_element_by_tag_name("span").text
            info = spec.find_element_by_tag_name("div").text
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
                        self._append_jsonl_file("tgdd_used.jsonl", result)
                    elif isinstance(result, str):
                        self._log_errors("tgdd_log.txt", result)
            except:
                print("Lỗi load trang")

            self._go_to_first_tab()


self = TGDD_Scraper()
self.parse(export=True)
