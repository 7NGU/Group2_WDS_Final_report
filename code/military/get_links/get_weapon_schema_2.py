from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
import time
import pymongo

categories = ['飞行器', '舰船舰艇', '枪械与单兵', '坦克装甲车辆', '火炮', '导弹武器', '太空装备', '爆炸物']
linkText = ['aircraft', 'warship', 'guns', 'tank', 'artillery', 'missile', 'spaceship', 'explosive']

def store_relation(category, sub_category, myco):
    myco.insert_one({"name": category , "subclass": sub_category})

def switch_category(browser, current_category_index):
    if current_category_index != 0:
        bt = browser.find_element_by_link_text(categories[current_category_index])
        bt.click()
        time.sleep(1)

def main():
    #浏览器打开
    # chromeOptions = Options()
    # chromeOptions.add_argument('C:/Users/92898/AppData/Local/Google/Chrome/User Data/Default/extension')
    # browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get('http://weapon.huanqiu.com/weaponlist')
    wait = WebDriverWait(browser, 10)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["military"]
    myco = mydb['schema_2']
    #类目遍历
    for index in range(len(categories)):
        #类目转换
        switch_category(browser, index)
        html = etree.HTML(browser.page_source, etree.HTMLParser())
        sub_category = html.xpath('//div[@class="select"]/ul[li[text()="大分类："]]/li/span[@class="list"]/a/text()')
        for s_ca in sub_category:
            store_relation(categories[index], s_ca, myco)
    myclient.close()

if __name__ == "__main__":
    main()
