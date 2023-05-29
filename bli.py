User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0'

Cookie = "buvid3=DB5DE49A-DC03-F90E-A46D-EE35CE48FFD294524infoc; b_nut=1681905994;\
        i-wanna-go-back=-1; _uuid=8D4104ABA-BA51-4192-1C101-518CEC1F3D8F92625infoc; \
        FEED_LIVE_VERSION=V8; home_feed_column=5; buvid4=62516266-523A-C594-D513-\
        B014F1126D6095381-023041920-tzUqlq9E3xrdhwGViB1vbg^%^3D^%^3D; CURRENT_FNVAL\
        =4048; CURRENT_PID=70e85710-df61-11ed-b718-a1cc6e2c9f86; rpdid=^|(u))~u^|\
        ukYk0J'uY)um)RluR; DedeUserID=1808739723; DedeUserID__ckMd5=11b819818f9a6db6; \
        CURRENT_QUALITY=80; b_ut=5; header_theme_version=CLOSE; SESSDATA=29edc109^%\
        ^2C1700657202^%^2C868c6^%^2A51; bili_jct=cfd3fcf7bdd7691176e171a44cb36e2b;\
        b_lsid=C2C410D9A_1885C05E89F; browser_resolution=1825-957; sid=6tjl2bqi; \
        bp_video_offset_1808739723=800262040841093100; fingerprint=64b1f10f941557\
        f6c23e2c80d66a351e; buvid_fp_plain=undefined; PVID=3; buvid_fp=64b1f10f94\
        1557f6c23e2c80d66a351e"

#headers
HEADERS = {
    'cookie' : Cookie,
    'user-agent' : User_Agent
    }


import re, requests
import pandas as pd
import time, datetime, os, shutil
from bs4 import BeautifulSoup

#计时
print('开始爬取')
time_start = time.time() #获得开始时间

URL = 'http://comment.bilibili.com/{cid}.xml' #格式化的弹幕网页

#获取网页源代码
def data_response(url, headers):
    try:
        response = requests.get(url, headers=HEADERS)
        response.encoding = 'utf-8' #设置文本编码为utf-8
        return response.text
    except:
        print('反爬虫机制已生效！ 请更换Cookies和UA！')
        
    
#获取视频cid（用于下一步获取弹幕网页）
def cid_data(url, headers):
    text = data_response(url, headers=HEADERS)
    cid = re.findall(r'"cid":(\d+),', text)[0]
    return cid

#限定时间范围
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
#search_time=dateRange("", "")


#读取bli.txt中的视频url
with open('bli.txt', mode='r', encoding='utf-8') as file:
     urls = file.readlines() 
     Barrage_urls = []
     cids = []
     for url in urls:
         cids.append(cid_data(url, headers=HEADERS)) #获取每个视频相应的cid
     for cid in cids:
         Barrage_urls.append(f'http://comment.bilibili.com/{cid}.xml'.format(cid)) #获取每个cid的网页信息

with open('cid.txt', mode='w', encoding=('utf-8')) as file: #将cid写入文档中
    j=0
    while(j < len(cids)):
        file.write(cids[j])
        file.write('\n')
        j+=1

i=0 #对cid计数
for url in Barrage_urls:
    time_data = [] #初始化时间列
    Barrage_list = [] #初始化内容列
    print(f'对于{url}:'.format(url))
    
    print('************正在处理数据************')
    soup = BeautifulSoup(data_response(url, headers=HEADERS), 'xml') #bf4解析网页
    Barrage_data = soup.find_all('d') #获取d标签的内容（UNIX时间戳与内容均在d标签里）
    time.sleep(2)

    print('***********共爬取{}条弹幕************'.format(len(Barrage_data)))
    time.sleep(2)

    for d in Barrage_data:
        data_split = d['p'].split(',') #将p标签分隔开
        temp_time = time.localtime(int(data_split[4])) #第3个为时间参数
        Barrage_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time) #格式化时间参数
        time_data.append(Barrage_time) 
        Barrage_list.append(d.text)
        
    CID = cids[i] 
    df = pd.DataFrame({'弹幕时间':time_data, '弹幕内容':Barrage_list}) #生成dataframe数据
    
    if os.path.isdir(f'{CID}'.format(CID)): #创建文件夹
        shutil.rmtree(f'{CID}'.format(CID))
        os.mkdir(f'{CID}'.format(CID))
    else :
        os.mkdir(f'{CID}'.format(CID))
    df.to_csv(f'{CID}\{CID}.csv'.format(CID), encoding='utf-8', index=False) #写入cid.csv文件中
    print('')
    print('')
    print('')
    print('')
    i += 1
  

time.sleep(2)
print('正在生成分析图......')
print('')
print('')
print('')
print('')
import day_dny
import enmotion_dny
import wordcloud_bar

print('处理完成！')
time.sleep(2)

time_end = time.time()
time_sum = time_end-time_start
print("共耗时:",time_sum,"s!")
print('')
print('')
print('')
print('')

ch = input('输入任意字符退出：')

    

	











