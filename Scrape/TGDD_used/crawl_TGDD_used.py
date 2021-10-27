import pandas as pd
import re
from Scrape.base_class import BaseScraper
from Scrape import convert


class TGDD_Scraper(BaseScraper):
    def __init__(self):
        super(TGDD_Scraper, self).__init__(driver_type="edge")
        self.driver.get("https://www.thegioididong.com/may-doi-tra/laptop")
        self._wait_and_click(".dong")
        try:
            while True:
                self._wait_and_click(".btnviewmoresp")
        except:
            self.laptops = self.driver.find_elements_by_css_selector('.products > li')

    def _parse_all_(self, sub_products, base_info):
        results = []
        for product in sub_products:
            try:
                self._wait_to_be_clickable(".products > li > div.imagebox")
                product.click()
                result = {}

                # Lấy tgian bảo hành còn lại + tình trạng của từng máy cũ
                self._wait_to_be_visible(".infosell")
                used_info = self.driver.find_elements_by_css_selector(".infosell")
                result["Bảo hành"] = ""
                result["Tình trạng"] = ""
                for info in used_info:
                    if "bảo hành:" in info.text.lower():
                        result["Bảo hành"] = info.text
                    elif "tình trạng máy" in info.text.lower():
                        result["Tình trạng"] = info.text
                print(result["Bảo hành"], result["Tình trạng"])

                self._wait_to_be_clickable(".priceused")

                result["Giá đã qua sử dụng"] = self.driver.find_element_by_class_name("priceused").text
                result.update(base_info)
                results.append(result)

                self._wait_to_be_no_longer_visible("div.loading-cart")
                self.driver.find_element_by_class_name("iconused-closed").click()
                self._wait_to_be_no_longer_clickable(".iconused-closed")
            except BaseException as e:
                # raise e
                failed_laptop = product.find_element_by_tag_name("img").get_attribute("alt")
                results.append(failed_laptop)
        return results

    def _parse_base_info(self, laptop):
        base_info = {}
        base_info["Tên"] = laptop.find_element_by_tag_name("h3").text
        base_info["Giá mới"] = laptop.find_element_by_tag_name("label").text

        savings = laptop.find_elements_by_css_selector("a > label:nth-child(6) > span")
        if savings:
            base_info["Tiết kiệm"] = savings[0].text

        self._go_to_new_tab(link=laptop.find_element_by_tag_name("a").get_attribute("href"))

        # Chuyển sang tab máy mới để:
        # - Lấy bảo hành mới
        new_laptop_link = self.driver.find_element_by_link_text("Xem chi tiết máy mới").get_attribute("href")
        self._go_to_new_tab(link=new_laptop_link)
        try:
            warranty = self.driver.find_element_by_css_selector(
                "ul.policy__list > li:nth-child(2) > p > b").text
            base_info["Bảo hành mới"] = warranty
        except:
            print("Không tìm thấy thông tin bảo hành")
        try:
            warranty = self.driver.find_element_by_css_selector(".warranty")
            if warranty:
                base_info["Bảo hành mới"] = warranty.text
        except:
            print("Không tìm thấy thông tin bảo hành")

        # - Lấy lấy phần trăm tiết kiệm để tính giá mới
        print(base_info["Bảo hành mới"])
        if "ngừng" in base_info["Giá mới"]:

            discount = self.driver.find_elements_by_css_selector(".box_oldproduct > a > i > b")
            if discount:
                base_info["Tiết kiệm"] = discount[0].text

        self.driver.close()
        self._go_to_last_tab()
        self.driver.close()
        self._go_to_first_tab()
        return base_info

    def _parse_similar_specifications_of_(self, products):
        specifications = {}
        products[0].click()
        self._wait_to_be_visible(".wrap_content")
        self._wait_and_click(".viewparameterfull")
        self._wait_to_be_visible(".parameterfull > li[class]")

        specs = self.driver.find_elements_by_css_selector(".parameterfull > li[class]")
        for spec in specs:
            name = spec.find_element_by_tag_name("span").text
            info = spec.find_element_by_tag_name("li>div").text
            specifications[name] = info

        self._wait_to_be_no_longer_visible("div.loading-cart")
        self.driver.find_element_by_class_name("iconused-closed").click()
        self._wait_to_be_no_longer_clickable(".iconused-closed")
        return specifications

    def parse(self, *args, export=False) -> None:
        for laptop in self.laptops:
            try:

                base_info = self._parse_base_info(laptop)

                self._go_to_new_tab(link=laptop.find_element_by_tag_name("a").get_attribute("href"))
                sub_products = self.driver.find_elements_by_css_selector(".products > li > div.imagebox")

                specifications = self._parse_similar_specifications_of_(sub_products)
                base_info.update(specifications)

                #TODO: Có thể gom 1 đống bên trên vào parse_all??

                results = self._parse_all_(sub_products, base_info)
                self._write(results)

            except BaseException as e:
                # raise e
                print("Lỗi load trang")
            finally:
                self.driver.close()

            self._go_to_first_tab()

    def _write(self, results):
        for result in results:
            if isinstance(result, dict):
                self._append_jsonl_file("TGDD_used.jsonl", result)
            elif isinstance(result, str):
                self._log_errors("TGDD_used_log.txt", result)


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