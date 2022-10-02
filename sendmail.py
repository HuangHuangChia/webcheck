#coding=utf-8
from email.mime.text import MIMEText#專門傳送正文
from email.mime.multipart import MIMEMultipart#傳送多個部分
from email.mime.application import MIMEApplication#傳送附件
import smtplib#傳送郵件
import os

def _sendmail(send_user = 'WebPage Test<Doraemon@typc.mohw.gov.tw>' ,receive_users = '<honga@typc.mohw.gov.tw>',
              subject = 'Python email 測試',email_text = '這是菜鳥教程Python 郵件傳送測試……',
              server_address = 'msa.hinet.net',file = 'D:\\temp\\test1.txt' ):
#file = 'D:\\temp\\test1.txt' #附件路徑
#file1 = 'C:\\Users\\wm\\Desktop\\102.txt' #附件路徑

#send_user = u'多拉A夢<Doraemon@typc.mohw.gov.tw>'   #發件人
#password = '*************'   #授權碼/密碼
#receive_users = '皇嘉<honga@typc.mohw.gov.tw>'   #收件人，可為list
#subject = 'Python email test'  #郵件主題
#email_text = '這是菜鳥教程Python 郵件傳送測試……'   #郵件正文
#server_address = 'msa.hinet.net'   #伺服器地址
    mail_type = '1'    #郵件型別

    #構造一個郵件體：正文 附件
    msg = MIMEMultipart()
    msg['Subject']=subject     #主題
    msg['From']=send_user      #發件人
    msg['To']=receive_users    #收件人

    #構建正文
    part_text=MIMEText(email_text)
    msg.attach(part_text)             #把正文加到郵件體裡面去

    #構建郵件附件
    #filename = file           #獲取檔案路徑
    #  檢查檔案是否存在
    if os.path.isfile(file):  
        part_attach1 = MIMEApplication(open(file,'rb').read())   #開啟附件
        part_attach1.add_header('Content-Disposition','attachment',filename=file) #為附件命名
        msg.attach(part_attach1)   #新增附件

    # 傳送郵件 SMTP
    smtp= smtplib.SMTP(server_address,25)  # 連線伺服器，SMTP_SSL是安全傳輸

    #smtp.login(send_user, password)
    smtp.sendmail(send_user, receive_users, msg.as_string())  # 傳送郵件
    #print('郵件傳送成功！')
    
#_sendmail()
