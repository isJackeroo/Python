import requests
import re
from requests.exceptions import RequestException
import pandas as pd
import json
import csv
from time import sleep

# 抓取单页内容
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    try:
        response = requests.get(url,headers=headers)
        response.encoding='utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def get_city():
    # 武汉：wh  北京：bj 上海：sh
    city_name = input('请输入城市名称，例如上海，北京，武汉等：')
    city_en = getPinyin(city_name)
    print(city_en)

    # 需要查询多少页面
    num = input('查询的页数:')
    print(num)

    return city_en, int(num)


def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''

def getPinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    return ''.join(charLst)

# 使用正则表达式解析网页https://wh.fang.lianjia.com/loupan/pg2/
def parse_one_page_loupan():
    html_list = []
    city, num = get_city()
    for i in range(1,num,1):
        url = 'https://'+city+'.lianjia.com/loupan/pg'+str(i)
        print(url)
        html = get_one_page(url)
        # print(html)
        # https: // wh.fang.lianjia.com / loupan / p_whjycbjybt /?fb_expo_id = 427595620014956544
        pattern = re.compile('class="resblock-img-wrapper " title="(.*?)".*?<div class="resblock-name.*?<a href="(.*?)/" class="name.*?fb_expo_id&quot;:&quot;(.*?)&quot;.*?<span class="resblock-type".*?">(.*?)</span>.*?<span class="sale-status".*?">(.*?)</span>.*?fb_ab_test_flag.*?">(.*?)</a>.*?fb_ab_test_flag.*?<span>(.*?)</span>.*?/</i>.*?<span>(.*?)</span>.*?div class="resblock-area.*?<span>(.*?)</span>.*?<span class="number">(.*?)</span>.*?<div class="second">(.*?)</div>', re.S)
        print(f"--------------开始打印第{i}页--------------")
        items = re.findall(pattern,html)
        print(items)
        for item in items:
            print(item)
            html_dict = {}
            html_dict['html_url'] = 'https://wh.fang.lianjia.com'+item[1].strip()+'/?fb_expo_id='+item[2].strip()
            html_dict['html_loupan'] = item[0].strip()
            html_dict['html_yongtu'] = item[3].strip()
            html_dict['html_zhuangtai'] = item[4].strip()
            html_dict['html_dizhi'] = item[5].strip()
            html_dict['html_type'] = item[6].strip()+'/'+item[7].strip()
            html_dict['html_mianji'] = item[8].strip()
            html_dict['html_junjia'] = item[9].strip()
            html_dict['html_zongjia'] = item[10].strip()
            html_list.append(html_dict)
        sleep(1)
    print(html_list)
    print('-----------------打印完成----------------')
    return html_list

# 写入并保存至文件
# 保存为txt格式
def html_to_csv():
    items = parse_one_page_loupan()
    df = pd.DataFrame(items)
    df.columns = ['链接','楼盘','性质','状态','地址','类型','面积','房子均价','房子总价']
    # print(df)
    df.to_excel('./lianjia_newroom03.xlsx',sheet_name='20210324',index=False)

# 定义主函数
def main():
    html_to_csv()

if __name__ == '__main__':
        main()
