import pandas as pd
from Scrape.utils.base_class import BaseScraper
from Scrape.utils import convert


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
                self._wait_to_be_clickable(".products > li")
                result = {}

                # Lấy tgian bảo hành còn lại + tình trạng của từng máy cũ
                used_info = product.find_elements_by_tag_name("label")
                result["Bảo hành cũ"] = ""

                for info in used_info:
                    if "bảo hành:" in info.text.lower():
                        result["Bảo hành cũ"] = info.text

                result["Giá máy cũ"] = product.find_element_by_css_selector("div:nth-child(2)").text
                result.update(base_info)
                results.append(result)
            except BaseException as e:
                # raise e
                failed_laptop = product.find_element_by_tag_name("img").get_attribute("alt")
                results.append(failed_laptop)
        return results

    def _parse_base_info(self, laptop):
        base_info = {}
        base_info["Tên"] = laptop.find_element_by_tag_name("h3").text
        base_info["Giá máy mới"] = laptop.find_element_by_tag_name("label").text

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
            print("")
        try:
            warranty = self.driver.find_element_by_css_selector(".warranty")
            if warranty:
                base_info["Bảo hành mới"] = warranty.text
        except:
            # print("Không tìm thấy thông tin bảo hành")
            print("")

        # - Lấy lấy phần trăm tiết kiệm để tính giá mới
        # print(base_info["Bảo hành mới"])
        if "ngừng" in base_info["Giá máy mới"]:

            discount = self.driver.find_elements_by_css_selector(".box_oldproduct > a > i > b")
            if discount:
                base_info["Tiết kiệm"] = discount[0].text

        specs = self._parse_similar_specifications()
        base_info.update(specs)

        self.driver.close()
        self._go_to_last_tab()

        return base_info

    def _parse_similar_specifications(self):
        specifications = {}
        self._wait_and_click(".btn-short-spec")
        self._wait_to_be_visible(".parameter-all li")
        specs = self.driver.find_elements_by_css_selector(".parameter-all li")
        for spec in specs:
            name = spec.find_element_by_class_name("ctLeft").text[:-1]
            info = spec.find_element_by_class_name("ctRight").text
            specifications[name] = info

        return specifications

    def parse(self, *args, export=False) -> None:
        num_laptops = len(self.laptops)
        for index, laptop in enumerate(self.laptops):
            if index == 2:
                print(f'Đã crawl xong 2 loại máy laptops.\n Cám ơn thầy đã xem')
                break
            try:
                print(f'Crawling {index + 1}/{num_laptops}...')
                base_info = self._parse_base_info(laptop)
                sub_products = self.driver.find_elements_by_css_selector(".products > li")
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

# %% Convert raw jsonlines to csv

raw_data = convert.read_results("Scrape/TGDD_used/TGDD_used.jsonl")
max_columns = convert.get_spec_fields(raw_data)
df = convert.make_frame(raw_data, max_columns)
df.to_csv("raw_data_TGDD_all_used.csv", index=False)

# %%

# Lấy trung bình giá cũ của các máy cùng loại
df = pd.read_csv("Dataset/Raw/raw_data_TGDD_used_renamed.csv")
df_take_first_occurence = df.groupby("name")[df.columns].first()

df.to_csv("raw_data_TGDD_used.csv", index=False)
