# -*- coding: utf-8 -*-
__author__ = 'JYC'

import codecs
import datetime
import os
from encrypt_account import DES
from my_smtp import Sender

def title_mail(now):
    return " YY년 MM월 원격점검표입니다.".replace('YY', str(now.year)).replace('MM', '{0:0>2}'.format(now.month))

def body_mail(now):
    return'''안녕하십니까

테크하임입니다.

YY년 MM월 원격점검표 아래에 첨부해드립니다.

감사합니다.'''.replace('YY', str(now.year)).replace('MM', '{0:0>2}'.format(now.month))

def is_mail_info_valid(mail_info, att):
    if not os.path.isfile(att):
        print(att + ' 는 존재하지 않는 파일입니다.')
        return False
    elif mail_info[0][0] == '#':
        print(mail_info[0] + ' 가 주석처리되었으므로 메일을 전송하지 않고 넘어갑니다.')
        return False
    elif '@' not in mail_info[1] or '.' not in mail_info[1]:
        print(mail_info[0] + ' 의 메일 주소를 제대로 입력해주세요.')
        return False
    return True

now = datetime.datetime.now()

#read and decrypt id and pw
des = DES()
f = open('account_info', 'r')
account_list = f.readlines()
account_list[0] = des.decrypt(account_list[0].encode()).decode()
account_list[1] = des.decrypt(account_list[1].encode()).decode()
f.close()

#make sender object Sender(ID, PW)
sender = Sender(account_list[0], account_list[1])

f = codecs.open("mailing_list", 'r', 'utf-8')
mailing_list = f.readlines()

count = 0
for info_line in mailing_list:
    mail_info = info_line.strip().split(':')
    mail_info[2] = mail_info[2].replace('YY', str(now.year)).replace('MM', '{0:02}'.format(now.month))
    if count == 0:
        mail_info[0] = mail_info[0][1:]
    if not is_mail_info_valid(mail_info, mail_info[2]):
        continue

    try:
        sender.send_gmail(mail_info[1], mail_info[0] + title_mail(now), body_mail(now), 'html', mail_info[2])
        print(os.path.basename(mail_info[2])  + " 가 첨부되어 발송될 예정입니다." + mail_info[2].split('\\')[-1])
        print(mail_info[1] + " 으로 첨부파일과 함꼐 메일을 발송하였습니다.")
        pass
    except:
        print("sender.send_gmail raised exception!!")

    #                                여기가 제목             text = 본문 ,
    count = count + 1
