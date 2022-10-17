import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pandas as pd
from selenium.webdriver.common.by import By
import csv


def get_url():
    url = 'http://www.taobao.com'  # 输入要爬取的网址
    Myoptions = webdriver.ChromeOptions()  # 如果网站反爬，需要修改浏览器的参数，让NAVIGATOR不能检测到是自动脚本
    Myoptions.add_argument('--disable-blink-features=AutomationControlled')  # 需要录入的参数
    wb = webdriver.Chrome(options=Myoptions)  # 把新的参数传给启动的浏览器
    wb.get(url)
    print('淘宝网页已经获取，准备登录中。。。')
    wb.implicitly_wait(5)
    get_login(wb)

def get_login(wb):
    username = 'sprng888'  # 设置好用户名和密码
    password = 'wlsl1314520lp'
    wb.find_element(By.CLASS_NAME,'h').click()  # 进入页面后，通过F12找到登录的按钮。PYTHON新的版本需要用到FIND_ELEMENT(BY)这个包，区分ELEMENT和ELEMENTS不同，后者返回的是列表
    print('进入登录页面')
    time.sleep(2)
    iframe = wb.find_element(By.CLASS_NAME, 'reg-iframe')  # 由于登录窗口是嵌套的网页，里面有IFRAME，因此需要用这个方法定位到IFRAME
    wb.switch_to.frame(iframe)  # 把WB转到定位后的IFRAME，这样才可以对下面的用户名和密码进行操作
    wb.find_element(By.NAME, 'fm-login-id').send_keys(username)  # 找到用户名录入的地方并将已经设置好的用户名传进去
    wb.find_element(By.ID, 'fm-login-password').send_keys(password)  # 找到密码的录入地方，将密码传进去
    wb.find_element(By.CLASS_NAME, 'fm-btn').click()  # 找到登录按钮然后点击进入
    wb.implicitly_wait(10)
    print('——————————————  用户登录成功  ———————————————')
    get_product(wb,serch_content)

def get_product(wb,serch_content):
    print(serch_content, '正在查询中。。。。。。。。。')
    wb.switch_to.default_content()  # 从IFRAME切换回默认的设置
    wb.switch_to.window(wb.window_handles[0])
    wb.find_element(By.CLASS_NAME, 'searchbar-input').send_keys(serch_content)
    time.sleep(2)
    wb.find_element(By.CLASS_NAME, 'rax-text-v2.search-button-text').click()
    print('已经找到',serch_content)
    time.sleep(2)
    get_data(wb)

def get_data(wb):
    product_report = {'商品图片': [], '商品名称': [], '商品价格': [], '商品成交量': [], '卖家位置': []}  #用字典的形式把数据保存起来以便EXCEL识别
    product_list = wb.find_elements(By.ID, 'mainsrp-itemlist')  # 遍历时一定要用复数，而不能是element
    print('正在爬取所需商品信息。。。。。。')
    page = 0
    for page in range(10):
        for items in product_list:
            for i in range(44):
                pic = items.find_elements(By.CLASS_NAME, 'J_ItemPic')  # 这里find_elements 一定要和上面一致，否则会报错
                pic = pic[i].get_attribute('src')  # find_elements或者复数后面不能使用get_attribute指令来获取属性
                product_report['商品图片'].append(pic)

                product_name = items.find_elements(By.CLASS_NAME, 'J_ItemPic') #获取产品名字
                product_name = product_name[i].get_attribute('alt')
                product_report['商品名称'].append(product_name)   #把产品名字加入字典中，下同

                product_price = items.find_elements(By.CLASS_NAME, 'price')   #获取产品价格
                product_price = product_price[i].text
                product_report['商品价格'].append(product_price)

                product_amount = items.find_elements(By.CLASS_NAME, 'deal-cnt')  #获取产品销售数量
                product_amount = product_amount[i].text
                product_report['商品成交量'].append(product_amount)

                product_place = items.find_elements(By.CLASS_NAME, 'location')   #获取商家的位置
                product_place = product_place[i].text
                product_report['卖家位置'].append(product_place)

            print('第{}页商品信息爬取成功'.format(page + 1))   #显示第几页已经爬取到所需信息
            time.sleep(2)
            pl = pd.DataFrame(product_report)
        # pl.to_csv('.\{}.csv'.format(serch_content),encoding='utf-8-sig')  #保存信息到CSV格式中，UTF这里需要加SIG，否则会出现乱码）
        pl.to_excel('.\{}.xlsx'.format(serch_content),encoding='utf-8')
        print('第%d页信息保存成功'%(page+1))
        print('开始查找下一页')
        page += 1
        wb.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[2]/input').clear()
        wb.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[2]/input').send_keys(page+1)
        wb.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]').click()


        # wb.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a').click()  #第5页开始XPATH路径会有变动，LI【8】中间的数字会每页增加1，因此报错无法定位到该位置
        time.sleep(5)
        print('找到第%d页'%(page+1))
        wb.implicitly_wait(10)

    print('任务完成！！！')


if __name__ == '__main__':
    serch_content = input ('请输入要查询的物品信息：')
    print('开始进入淘宝首页。。。。。。')
    get_url()





