#EnglishVersion
import requests
import codecs
from bs4 import BeautifulSoup
from datetime import datetime
import pathlib
import sendmail
import os

change=['<span>Current Number：<img src="/english/images/counter/12/','<span>Update：']

currentpath=str(pathlib.Path().absolute())+"\\"

url='https://www.typc.mohw.gov.tw/english/'

path=currentpath+"Typc_Eng_Html_old.txt"

path1=currentpath+"Typc_Eng_Html_new.txt"

path_counter=currentpath+"Typc_Eng_counter.txt"
path_error=currentpath+"Typc_Eng_error.txt"
path_status=currentpath+"Typc_Eng_info.txt"

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
f2.write("官網EnglishVersion"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+",瀏覽人數:"+count+','+a[-1].text+"\n")

status=0
i=0

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


notify="官網EnglisgVersion"

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
