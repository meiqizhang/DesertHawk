#encoding=utf-8
import smtplib
import time
from email.mime.text import MIMEText

import pymysql

from DesertHawk.settings import DATABASES

def db_connect():
    database = DATABASES.get("default")

    connect = pymysql.Connect(
        host=database['HOST'],
        port=int(database['PORT']),
        user=database['USER'],
        passwd=database['PASSWORD'],
        db=database['NAME'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connect

today = time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time()))

msg_from = '164529140@qq.com'  # 发送方邮箱
passwd = 'hdkenufzgibrbgii'  # 填入发送方邮箱的授权码
msg_to = 'zhangqi_gsts@foxmail.com'  # 收件人邮箱

subject = "网站访客报表"
sql = "select * from t_site_statistic where visit_time > %s order by id"

connect = db_connect()
cursor = connect.cursor()
cursor.execute(sql, today)
records = cursor.fetchall()

content = "今日有 %d 位访客" % cursor.rowcount

msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print("发送成功")
except Exception as e:
    print("发送失败, e=%s" % e)
finally:
    s.quit()