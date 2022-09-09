import django
import os
import json
import datetime
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'telebot_project.settings'
django.setup()


import telebot
from telegram_bot.models import *

API_KEY = '5546573583:AAHh0Z8q7NCXGrievNTu9ptVAiZBLKyoAZ4'

bot = telebot.TeleBot(API_KEY)
# Create your models here.

class mainAppInfo:
  def __init__(self, RegProccess, step, FIRST_NAME, LAST_NAME, MOBILE_NUM, EDU_TEXT, FIELD_TEXT, PLACE_TEXT):
    self.RegProccess = RegProccess
    self.step = step
    self.FIRST_NAME = FIRST_NAME
    self.LAST_NAME = LAST_NAME
    self.MOBILE_NUM = MOBILE_NUM
    self.EDU_TEXT = EDU_TEXT
    self.FIELD_TEXT = FIELD_TEXT
    self.PLACE_TEXT = PLACE_TEXT

class app_dic:
    def __init__(self, 
        hello_m, 
        first_m, 
        first_name_m, 
        last_name_m, 
        mobile_number_m,
        mobile_guid_m, 
        mobile_number_inccorect_m,
        edu_m,
        field_m,
        place_m,
        success_step_m,
        last_m):
        self.hello_m = hello_m
        self.first_m = first_m
        self.first_name_m = first_name_m
        self.last_name_m = last_name_m
        self.mobile_number_m = mobile_number_m
        self.mobile_guid_m = mobile_guid_m
        self.mobile_number_inccorect_m = mobile_number_inccorect_m
        self.edu_m = edu_m
        self.field_m = field_m
        self.place_m = place_m
        self.success_step_m = success_step_m
        self.last_m = last_m



appInfo = mainAppInfo(
False,
0,
'',
'',
'',
'',
'',
''
)

app_dic_txt = app_dic(
    'مراحل رو بابت ثبت نام شروع کنید',
    'لطفا اطلاعات خود را بابت کد تخفیف وارد نمایید',
    'لطفا نام خود را وارد نمایید',
    'لطفا نام خانوادگی خود را وارد نمایید',
    'لطفا شماره تماس خود را وارد نمایید',
    'لطفا شماره تماس خود را با فرمت 09121111111 وارد نمایید',
    'لطفا شماره تماس خود را درست وارد نمایید',
    'لطفا میزان تحصیلات خود را وارد نمایید',
    'لطفا رشته تحصیلی خود را وارد نمایید',
    'لطفا آدرس خود را وارد نمایید',
    'با موفقیت ثبت شد',
    'اطلاعات شما به صورت کامل ثبت شد، خیلی ممنونم',
)


def check_phone_number(phoneNumbers):
    return re.search("^(?:\+?44)?[07]\d{9,13}$", phoneNumbers)
    

@bot.message_handler(commands=['Reg'])
def register_user(message):
    appInfo.RegProccess = True
    bot.reply_to(message, app_dic_txt.first_m)
    bot.send_message(message.chat.id, app_dic_txt.first_name_m)


def check_text(message):
    if (appInfo.RegProccess):
        if(appInfo.step == 0):
            appInfo.FIRST_NAME = message.json['text']
            appInfo.step += 1
        if(appInfo.step == 1):
            bot.send_message(message.chat.id, app_dic_txt.success_step_m)
            bot.send_message(message.chat.id, app_dic_txt.last_name_m)
            appInfo.LAST_NAME = message.json['text']
            appInfo.step += 1
        elif(appInfo.step == 2):
            bot.send_message(message.chat.id, app_dic_txt.mobile_number_m)
            bot.send_message(message.chat.id, app_dic_txt.mobile_guid_m)
            if check_phone_number(message.json['text']):
                bot.send_message(message.chat.id, app_dic_txt.success_step_m)
                appInfo.MOBILE_NUM = message.json['text']
                appInfo.step += 1
            else:
                bot.send_message(message.chat.id,app_dic_txt.mobile_number_inccorect_m)    
        elif(appInfo.step == 3):
            bot.send_message(message.chat.id, app_dic_txt.success_step_m)
            bot.send_message(message.chat.id, app_dic_txt.edu_m)
            appInfo.EDU_TEXT = message.json['text']
            appInfo.step += 1
        elif(appInfo.step == 4):
            bot.send_message(message.chat.id, app_dic_txt.success_step_m)
            bot.send_message(message.chat.id, app_dic_txt.field_m)
            appInfo.FIELD_TEXT = message.json['text']
            appInfo.step += 1
        elif(appInfo.step == 5):
            bot.send_message(message.chat.id, app_dic_txt.success_step_m)
            bot.send_message(message.chat.id, app_dic_txt.place_m)
            appInfo.PLACE_TEXT = message.json['text']
            appInfo.step += 1
        else:
            new_teleUser = Telebot_Users(
                Name = appInfo.FIRST_NAME,
                Family_Name = appInfo.LAST_NAME,
                Mobile_Number = appInfo.MOBILE_NUM,
                Education = appInfo.EDU_TEXT,
                Field = appInfo.FIELD_TEXT,
                Location = appInfo.PLACE_TEXT,
                Status = 'P'
            )
            new_teleUser.save()
            bot.send_message(message.chat.id, app_dic_txt.last_m)
            appInfo.RegProccess = False
            appInfo.step = 0
    else:
        return False

@bot.message_handler(func=check_text)
def test_users(message):
    bot.reply_to(message, app_dic_txt.hello_m)

bot.polling()