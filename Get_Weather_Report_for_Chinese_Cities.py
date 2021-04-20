# -*- coding: utf-8 -*-
"""
    learn python:tianqi
    <通过天气网的接口，制作专属天气预报，可以对接树莓派哦，搞个屏幕>
    :copyright: (c) 2019 by learn python.
    :license: GPLv3, see LICENSE File for more details.
"""

import requests
from lxml import etree

requests.packages.urllib3.disable_warnings()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}


def getText(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return "".join(rc)


def get_weather_info(addr):
    global weather_info, today, date
    url = "https://www.tianqi.com/" + str(addr)
    responese = requests.get(url, headers=headers, verify=False)
    html = responese.text
    selector = etree.HTML(html)
    try:
        name = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="name"][1]/h2[1]/text()'
        )[0]
        date_rili = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="week"]/text()'
        )[0]
        now_temp = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="weather"][1]/p[@class="now"][1]/b[1]/text()'
        )[0]
        now_w = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="weather"][1]/span[1]/b[1]/text()'
        )[0]
        today_temp = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="weather"][1]/span[1]/text()'
        )[0]
        dampness = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="shidu"][1]/b[1]/text()'
        )[0]
        now_wind = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="shidu"][1]/b[2]/text()'
        )[0]
        now_sunshine = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="shidu"][1]/b[3]/text()'
        )[0]
        air = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="kongqi"][1]/h5[1]/text()'
        )[0]
        pm = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="kongqi"][1]/h6[1]/text()'
        )[0]
        node = selector.xpath(
            '//div[@class="weatherbox"][1]/div[@class="wrap1100"][1]/div[@class="left"][1]/dl[@class="weather_info"][1]/dd[@class="kongqi"][1]/span[1]'
        )[0]
        sun_s = getText(node)
        sun_richu = sun_s.split("日落")[0]
        sun_riluo = "日落" + str(sun_s.split("日落")[1])
        date = []
        for i in range(1, 8):
            date_list = []
            date_data = selector.xpath('//ul[@class="week"][1]/li[%d]/b[1]/text()' % i)[
                0
            ]
            date_week = selector.xpath('//ul[@class="week"][1]/li[%d]/span/text()' % i)[
                0
            ]
            date_list.append(date_data)
            date_list.append(date_week)
            date.append(date_list)
        weather = []
        for i in range(1, 8):
            weather_data = selector.xpath(
                '//ul[@class="txt txt2"][1]/li[%d]/text()' % i
            )[0]
            weather.append(weather_data)
        temp = []
        for i in range(1, 8):
            temp_data = []
            temp_high = selector.xpath(
                '//div[@class="zxt_shuju"][1]/ul[1]/li[%d]/span[1]/text()' % i
            )[0]
            temp_low = selector.xpath(
                '//div[@class="zxt_shuju"][1]/ul[1]/li[%d]/b[1]/text()' % i
            )[0]
            temp_data.append(temp_high)
            temp_data.append(temp_low)
            temp.append(temp_data)
        wind = []
        for i in range(1, 8):
            wind_data = selector.xpath('//ul[@class="txt"][1]/li[%d]/text()' % i)[0]
            wind.append(wind_data)
        weather_info = """
        %s   %s
************************************************
+                       温度：%s
+                       天气情况：%s
+                       温度范围：%s
+                       %s
+                       %s
+                       %s
+                       %s
+                       %s
+                       %s
+                       %s
-----------------------------------------------------------------------
                   %s  未来7天的天气
-----------------------------------------------------------------------
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
【%s %s：%s , 最高气温：%s , 最低气温：%s ， %s】
-----------------------------------------------------------------------
""" % (
            name,
            date_rili,
            now_temp,
            now_w,
            today_temp,
            dampness,
            now_wind,
            now_sunshine,
            air,
            pm,
            sun_richu,
            sun_riluo,
            name,
            date[0][0],
            date[0][1],
            weather[0],
            temp[0][0],
            temp[0][1],
            wind[0],
            date[1][0],
            date[1][1],
            weather[1],
            temp[1][0],
            temp[1][1],
            wind[1],
            date[2][0],
            date[2][1],
            weather[2],
            temp[2][0],
            temp[2][1],
            wind[2],
            date[3][0],
            date[3][1],
            weather[3],
            temp[3][0],
            temp[3][1],
            wind[3],
            date[4][0],
            date[4][1],
            weather[4],
            temp[4][0],
            temp[4][1],
            wind[4],
            date[5][0],
            date[5][1],
            weather[5],
            temp[5][0],
            temp[5][1],
            wind[5],
            date[6][0],
            date[6][1],
            weather[6],
            temp[6][0],
            temp[6][1],
            wind[6],
        )
        print(weather_info)
    except Exception as e:
        print(str(e))
    today = date[0][0]


city = ["chengdu"]
# import smtplib
# from email.mime.text import MIMEText

# mailto_list=''
# mail_host=""
# mail_user="****"
# mail_pass="*************"
# mail_postfix=""

weather_info_all = """"""
for i in city:
    get_weather_info(i)
    weather_info_all = weather_info_all + weather_info
    # try:
    #         msg = MIMEText(weather_info_all)
    #         msg["Subject"] = today + "天气预报"
    #         msg["From"]    = mail_user
    #         msg["To"]      = mailto_list
    #         s = smtplib.SMTP_SSL(mail_host,465)
    #         s.login(mail_user, mail_pass)
    #         s.sendmail(mail_user, mailto_list, msg.as_string())
    #         s.quit()
    # except Exception as e:
    #         print("Falied,%s"%e)
    # 并没有什么
