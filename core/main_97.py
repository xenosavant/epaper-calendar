#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import subprocess
import os
import math
import textwrap
from dateutil.parser import *
from datetime import datetime, timedelta
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
import calendar
import requests
import time
import json
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    payload = "[{\"id\":\"5d93a3aa35a2035a041fc1f5\",\"date\":\"2019-10-18T19:15:00.000Z\",\"endDate\": \"2019-10-18T00:00:00.000Z\",\"startTimeMinutes\": 915,      \"endTimeMinutes\": 1200,      \"timezone\": \"America\/New_York\",      \"utcOffset\": \"-04:00\",      \"billed\": \"2019-10-11T00:00:02.336Z\",      \"brandName\": \"McDonald's\",      \"businessPositionName\": \"Food Prep\",      \"locationName\": \"Gaskins\",      \"managerFullName\": \"Omar Owner\",      \"workerFullName\": \"William Worker\",      \"userId\": \"58067bb8cb9cd6e416e62ca3\",      \"groupCount\": 1,      \"startTime\": 15.25,      \"endTime\": 20,      \"totalBill\": 93.86    },    {      \"id\": \"5d93a39435a2035a041fc1f3\",      \"active\": false,      \"date\": \"2019-10-19T14:15:00.000Z\",      \"endDate\": \"2019-10-19T17:45:00.000Z\",      \"startTimeMinutes\": 315,      \"endTimeMinutes\": 685,      \"timezone\": \"America\/Chicago\",      \"utcOffset\": \"-05:00\",      \"brandName\": \"McDonald's\",      \"businessPositionName\": \"Busser\",      \"locationName\": \"Bon Air\",      \"managerFullName\": \"Omar Owner\",      \"workerFullName\": \"William Worker\",      \"userId\": \"58067bb8cb9cd6e416e62ca3\",      \"groupCount\": 1,      \"startTime\": 5.25,      \"endTime\": 11.4167,      \"totalBill\": 0    },    {      \"id\": \"5d926842ae645a0d75bdd235\",      \"active\": true,      \"date\": \"2019-10-02T15:30:00.000Z\",      \"endDate\": \"2019-10-02T21:30:00.000Z\",      \"startTimeMinutes\": 690,      \"endTimeMinutes\": 1050,      \"timezone\": \"America\/Chicago\",      \"utcOffset\": \"-05:00\",      \"billed\": \"2019-10-11T00:00:02.336Z\",      \"brandName\": \"McDonald's\",      \"businessPositionName\": \"Food Prep\",      \"locationName\": \"Bon Air\",      \"managerFullName\": \"Testy Mctesterson Jr\",      \"workerFullName\": \"William Worker\",      \"userId\": \"58067bb8cb9cd6e416e62ca3\",      \"groupCount\": 1,      \"startTime\": 11.5,      \"endTime\": 17.5,      \"totalBill\": 87.36    },    {      \"id\": \"5d9267f6ae645a0d75bdd233\",      \"active\": true,      \"date\": \"2019-10-20T20:45:00.000Z\",      \"endDate\": \"2019-10-20T23:30:00.000Z\",      \"startTimeMinutes\": 1005,      \"endTimeMinutes\": 1170,      \"timezone\": \"America\/New_York\",      \"utcOffset\": \"-04:00\",      \"billed\": \"2019-10-11T00:00:02.336Z\",      \"brandName\": \"McDonald's\",      \"businessPositionName\": \"Food Prep\",      \"locationName\": \"Gaskins\",      \"managerFullName\": \"Testy Mctesterson Jr\",      \"workerFullName\": \"William Worker\",      \"userId\": \"58067bb8cb9cd6e416e62ca3\",      \"groupCount\": 1,      \"startTime\": 16.75,      \"endTime\": 19.5,      \"totalBill\": 53.68    },    {      \"id\": \"5d8d0a7905d36c7e347b229a\",      \"active\": true,      \"date\": \"2019-10-22T19:00:00.000Z\",      \"endDate\": \"2019-10-22T21:30:00.000Z\",      \"startTimeMinutes\": 900,      \"endTimeMinutes\": 1050,      \"timezone\": \"America\/New_York\",      \"utcOffset\": \"-04:00\",      \"brandName\": \"McDonald's\",      \"businessPositionName\": \"Cashier\",      \"locationName\": \"Short Pump\",      \"managerFullName\": \"Omar Owner\",      \"workerFullName\": \"Jane Worker\",      \"userId\": \"5c4b1ac73f7c1e001002ef50\",      \"groupCount\": 1,      \"startTime\": 15,      \"endTime\": 17.5,      \"totalBill\": 0    }  ]"
    black = 0    
    gray1 = 32
    gray2 = 64
    gray3 = 96
    gray4 = 128
    gray5 = 160
    gray6 = 192
    gray7 = 224
    white = 255
    smallFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    mediumFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 25)
    largeFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 45)

    HBlackimage = Image.new('L', (1200, 825), 255)
    draw = ImageDraw.Draw(HBlackimage)

    # ~ response = requests.get('http://192.168.1.227')
    shifts = json.loads(payload)

    i = 1;
    now = datetime.now()
    today = now.date()
    currentDayOfTheWeek = today.weekday()
    calendarStart = today - timedelta(days = currentDayOfTheWeek)
    calendarEnd = calendarStart + timedelta(days = 13)
    currentDay = calendarStart
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    index = 0;
    for day in days:
        logging.info(days[index])
        draw.text((((index + 1) * 171) - (171 / 2), 1), days[index], font = smallFont, fill = black)
        index = index + 1
    
    while i < 15:
        shiftIndex = 0;
        if i < 8:
            cellTop = 25
        else:
            cellTop = 425
        cellLeft = 5 + (((i - 1) % 7) * 170)
        cellRight = cellLeft + 170
        cellBottom = cellTop + 400
        fill = white
        if today.day == currentDay.day:
            fill = gray7
        draw.rectangle([(cellLeft, cellTop), (cellRight, cellBottom)], fill = fill, outline=0)
        draw.rectangle([(cellLeft, cellTop), (cellRight, cellTop + 25)], fill = gray6, outline=0)
        draw.text((cellLeft, cellTop), str(currentDay.day), font = mediumFont, fill = black)
        # ~ drawblack.line((cellLeft, cellTop, cellRight, cellTop), fill = 0)
        # ~ drawblack.line((cellLeft, cellBottom, cellRight, cellBottom), fill = 0)
        # ~ drawblack.line((cellLeft, cellTop, cellLeft, cellBottom), fill = 0)
        # ~ drawblack.line((cellRight, cellTop, cellRight, cellBottom), fill = 0)
        # ~ while shiftIndex < len(shifts):
            # ~ if shiftDate.day == currentDay.day and shiftDate.month == currentDay.month:
                # ~ text1 = shift['businessPositionName'] + ' @ ' + shift['brandName'] + ' ' + shift['locationName'] + ' '
                # ~ text2 = str(starthours) + ':' + (str(startminutes) if startminutes else '00') + starttimeofday + ' - ' + str(
                    # ~ endhours) + ':' + (str(endminutes) if endminutes else '00') + endtimeofday
                # ~ lines = textwrap.wrap(text1, 30)
                # ~ for line in lines:
                    # ~ drawblack.text((74, offset), line, font = smallFont, fill = 0)
                    # ~ offset += 18
                    # ~ drawblack.text((74, offset), text2, font = smallFont, fill = 0)
                # ~ shift = shifts[shiftIndex]
                # ~ shiftDate = parse(shift['date']).date()
                # ~ startminutes = int(shift['startTimeMinutes'] % 60);
                # ~ starthours = int(math.floor(shift['startTimeMinutes'] / 60))
                # ~ if starthours > 12:
                    # ~ starthours -= 12
                    # ~ starttimeofday = 'PM'
                # ~ else:
                    # ~ starttimeofday = 'AM'
                # ~ endminutes = int(shift['endTimeMinutes'] % 60);
                # ~ endhours = int(math.floor(shift['endTimeMinutes'] / 60))
                # ~ if endhours > 12:
                    # ~ endhours -= 12
                    # ~ endtimeofday = 'PM'
                # ~ else:
                    # ~ endtimeofday = 'AM'
                        
                # ~ offset = top + 5
            # ~ shiftIndex += 1

        # ~ drawblack.text((10, top + 5), calendar.day_name[currentDay.weekday()][0:3], font = mediumFont, fill = 0)
        # ~ drawblack.text((10, bottom - 60), str(currentDay.day), font = largeFont, fill = 0)
        currentDay = currentDay + timedelta(days = 1)
        i += 1
    HBlackimage.save('calendar.bmp')
    subprocess.call('sudo ./driver/IT8951 0 0 calendar.bmp', shell=True)
    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
    

    
    
    
