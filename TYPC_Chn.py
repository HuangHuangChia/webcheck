#中文版
import requests
import codecs
from bs4 import BeautifulSoup
from datetime import datetime
import pathlib
import sendmail
import os

change=['<span>累計人數：<img src="/images/counter/12/','<span>最後更新：']
#change=[4750,4756]   #不比對的行數
#bulletin_Medical=[1454,1458,1462,1466,1480,1488,1492,1506,1514,1518,1532,1536,1540,1558,1562,1566,1588,1592]#醫療部
#bulletin_affairs=[1628,1632,1636,1640,1654,1658,1662,1666,1680,1684,1688,1692,1706,1710,1714,1718,1732,1736,1740,1744,1758,1762,1766,1770] #醫事部公告
#bulletin_Administrator=[1802,1806,1810,1828,1832,1836,1854,1858,1862,1866,1880,1884,1888,1892,1906,1910,1914,1932,1936,1940,1944]#管理部公告
#change=[2630]
currentpath=str(pathlib.Path().absolute())+"\\"
#change=[2630]

url='https://www.typc.mohw.gov.tw/'

path=currentpath+"Typc_Chn_Html_old.txt"

path1=currentpath+"Typc_Chn_Html_new.txt"

path_counter=currentpath+"Typc_Chn_counter.txt"
path_error=currentpath+"Typc_Chn_error.txt"
path_status=currentpath+"Typc_Chn_info.txt"

res=requests.get(url)
res.encoding = 'utf-8'


f = open(path1, mode="w",encoding="utf-8")
f.write(res.text)
f.close()

##############
soup=BeautifulSoup(res.text,features="html.parser")    
#找計數器
a=soup.find_all('img',align="top")
#print(str(a[1])[-4])
count=""
for t in a:
    count+=str(t)[-4]
#count=int(count)
print(count)

a=soup.find_all('span')
print(a[-1].text)   

f = open(path_counter, mode="a",encoding="utf-8")
f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+","+count+','+a[-1].text+"\n")
f.close()


f= open(path, mode='r',encoding='UTF-8')
content_old=f.readlines()
f.close()

f1= open(path1, mode='r',encoding='UTF-8')
content_new=f1.readlines()
f1.close()

f2 = open(path_error, mode="w",encoding="utf-8")
f2.write("官網中文版"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+",瀏覽人數:"+count+','+a[-1].text+"\n")

status=0
i=0
#bulletin_affairs_counter=0
#bulletin_Medical_counter=0
#bulletin_Administrator_counter=0
if len(content_new) != len(content_old):
    f2.write("新舊網頁長度不同,原行數"+str(len(content_old))+" 新行數"+str(len(content_new))+"\n")

while (i<len(content_new) and i<len(content_old))  :
    if (not(content_new[i] in content_old)): #新網頁某行是否包含在舊網頁
        chg_idx=0
        for chg in change:
            if (chg in content_new[i]):      #確認有異動的行是否是change[i]的子字串
                chg_idx=1                    #若是則idx=1,視為相同
        if (chg_idx==0) :
            f2.write("line "+str(i)+"\n")
            f2.write(content_old[i]+content_new[i])
            print("line",i)
            print(content_old[i],content_new[i])
            status+=1
    i+=1
f2.close()    
print('done')


notify="官網中文版"

if status==0 and len(content_new) == len(content_old):
    notify+="測試無異常"
    if(os.path.isfile(path_status)): #刪除狀態檔及比較內容檔
      os.remove(path_status)
#    if(os.path.isfile(path_error)):
#      os.remove(path_error)    
else:
    notify+="與前版比較"
    if len(content_new) != len(content_old):
        notify+="新舊網頁長度不同,原行數+"+str(len(content_old))+" 新行數"+str(len(content_new))+"."
    if status>0:
        notify+="有"+str(status)+"項不同"
    notify+=",請確認"
    with open(path_status, mode="w",encoding="utf-8") as f3:
        f3.write(notify)    
    sendmail._sendmail(send_user = 'WebPage Test<Doraemon@typc.mohw.gov.tw>' ,receive_users = '<info@typc.mohw.gov.tw>',
              subject = notify,email_text = notify,
              server_address = 'msa.hinet.net',file = path_error )    


#f3.close()
#如果確認無誤,刪除Html_old.txt,將Html_new.txtrename為 Html_old.txt
#第一次執行會error,但會產生Html_new.txt,Html,將Html_new.txtrename為 Html_old.txt

#sendmail._sendmail(send_user = 'WebPage Test<Doraemon@typc.mohw.gov.tw>' ,receive_users = '<honga@typc.mohw.gov.tw>','''''
'''  sendmail._sendmail(send_user = 'WebPage Test<Doraemon@typc.mohw.gov.tw>' ,receive_users = '<info@typc.mohw.gov.tw>',
              subject = notify,email_text = notify,
              server_address = 'msa.hinet.net',file = path_error )    
'''
