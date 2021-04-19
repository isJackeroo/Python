from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定url,获取网页数据
import xlwt  # 进行excel 操作
import _sqlite3  # 进行SQlite 数据库操作


def main():
    baseurl = 'https://movie.douban.com/top250?start='
    # 1 爬取网页
    datalist = getDate(baseurl)
    savepath = '豆瓣电影Top250.xls'
    # 3 保存数据
    saveData(datalist,savepath)

# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # .表示一个字符 * 表示会有很多字符 ?表示这种情况有0次或者1次
# 影片图片的链接
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片的评分
fingRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价的人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findIng = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getDate(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数 10次 一页25条
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码

        # 逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')
        # 查找符合要求的字符串，形成列表 class要加下划线表示 div 下面的 class = item的属性
        for i in soup.find_all('div', class_='item'):
            # print(i) # 测试查看电影item全部信息
            data = []  # 保存一部电影的所有的信息
            i = str(i)

            # link表示获取影片详情的超链接
            link = re.findall(findLink, i)[0]  # re库用来查找通过正则表达式查找指定的字符串
            data.append(link)  # 添加图片

            ImgSrc = re.findall(findImgSrc, i)[0]
            data.append(ImgSrc)  # 添加链接

            titles = re.findall(findTitle, i)  # 片名可能只有一个中文名 没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace('/', '')  # 去掉无关的符号
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名 留空

            rating = re.findall(fingRating, i)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, i)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findIng, i)
            if len(inq) != 0:
                inq = inq[0].replace('。','')  # 去掉句号
                data.append(inq) # 添加概述
            else:
                data.append(' ')

            bd = re.findall(findBd, i)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd) # 去掉<br/>
            bd = re.sub('/',' ',bd) # 替换/
            data.append(bd.strip()) # 去掉前后的空格

            datalist.append(data) # 把处理好的一部电影信息放到列表里
    # print(datalist)
    return datalist


# 得到指定一个URL的网页内容
# head 表示告诉豆瓣 我们是什么类型的服务器
def askURL(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, reason):
            print(e.reason)

    return html  # 这里一定要返回给这个网页 给这个传递的网页


# 保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 创建worlbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概述","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #  列名
    for i in range(0,250):
        print('第%d条'%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  # 数据

    book.save(savepath) # 保存

if __name__ == '__main__':  # 当程序执行时
    main()
    print('爬取完毕')
