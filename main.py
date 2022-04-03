from requests_html import HTMLSession
import json

url = "ITEM URL HERE"
type_item = "ITEM CATEGORY HERE"
aff_link = "AFF LINK HERE"

session = HTMLSession()
driver_ = session.get(url)


class ItemInformation:
    get_info_dic = {
        "TITLE": '//*[@id="productTitle"]',
        "PRICE": '//*[@id="corePrice_feature_div"]/div/span/span[2]',
        "ABOUT_ITEM": '//*[@id="feature-bullets"]/ul',
        "AVAILABILITY": '//*[@id="availability"]/span',
        "REVIEWS": '//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span',
        "INSIDE_BOX": '//*[@id="witb-content-list"]',
        "PICTURE": '//*[@id="landingImage"]'}
    add_info = {}

    def __init__(self, type_item_group=None, aff_link_url=None):
        self.type_item_group = type_item_group
        self.aff_link_url = aff_link_url

    def find_item_information(self):
        for info in ItemInformation.get_info_dic:
            if info != "TITLE":
                try:
                    ItemInformation.add_info[info] = (
                        driver_.html.xpath(ItemInformation.get_info_dic[info], first=True)).text.replace('"', "")
                    if info == "ABOUT_ITEM":
                        replace_text = ItemInformation.add_info[info].find("})")
                        ItemInformation.add_info[info] = ItemInformation.add_info[info][replace_text + 3:].split("\n")
                    elif info == "PRICE":
                        ItemInformation.add_info[info] = ItemInformation.add_info[info].replace("\n", ".")
                except:
                    ItemInformation.add_info[info] = "No information"
        ItemInformation.add_info["PICTURE"] = (
            driver_.html.xpath(ItemInformation.get_info_dic["PICTURE"], first=True).attrs['src'])
        ItemInformation.add_info["buy link"] = self.aff_link_url
        ItemInformation.add_info["category"] = self.type_item_group

    def find_repeat_item(self):
        ItemInformation.add_info["TITLE"] = (
            driver_.html.xpath(ItemInformation.get_info_dic["TITLE"], first=True)).text.replace('"', "")
        return ItemInformation.add_info["TITLE"]


amazon = ItemInformation(type_item, aff_link)

def write_json(data, filename="a_data_items.json"):
    with open(filename, "w", encoding='utf-8') as x:
        json.dump(data, x, indent=9)


with open("a_data_items.json", "r+", encoding='utf-8') as json_file:
    data = json.load(json_file)
    data_info = data["AmazonItems"]["Items"]
    if amazon.find_repeat_item() in [x['title'] for x in data_info]:
        print("Item already exist in the file")
    else:
        amazon.find_item_information()
        data_info.append({
            "title": amazon.add_info["TITLE"],
            "price": amazon.add_info["PRICE"],
            "review rating": amazon.add_info["REVIEWS"],
            "availability": amazon.add_info["AVAILABILITY"],
            "short info about product": amazon.add_info["ABOUT_ITEM"],
            "whats inside the box": amazon.add_info["INSIDE_BOX"],
            "main picture url": amazon.add_info["PICTURE"],
            "item url": aff_link,
            "item type": type_item
        })

write_json(data)
