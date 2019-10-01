#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
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
from waveshare_epd import epd7in5bc
import calendar
import requests
import time
import json
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:    
    epd = epd7in5bc.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)
    smallFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    mediumFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 25)
    largeFont = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 45)

    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    response = requests.get('http://192.168.1.227/sdjfnksdjfndskj')
    value = json.loads(response.content)
    logging.info(value)
    shifts = value['shifts']

    i = 1;
    now = datetime.now()
    currentDay = now.date()
    while i < 8:
        shiftIndex = 0;
        top = ((i-1)*91)
        bottom = top + 91
        while shiftIndex < len(shifts):
            shift = shifts[shiftIndex]
            shiftDate = parse(shift['date']).date()
            startminutes = int(shift['startTimeMinutes'] % 60);
            starthours = int(math.floor(shift['startTimeMinutes'] / 60))
            if starthours > 12:
                starthours -= 12
                starttimeofday = 'PM'
            else:
                starttimeofday = 'AM'
            endminutes = int(shift['endTimeMinutes'] % 60);
            endhours = int(math.floor(shift['endTimeMinutes'] / 60))
            if endhours > 12:
                endhours -= 12
                endtimeofday = 'PM'
            else:
                endtimeofday = 'AM'
                    
            offset = top + 5
            if shiftDate.day == currentDay.day and shiftDate.month == currentDay.month:
                text1 = shift['businessPositionName'] + ' @ ' + shift['brandName'] + ' ' + shift['locationName'] + ' '
                text2 = str(starthours) + ':' + (str(startminutes) if startminutes else '00') + starttimeofday + ' - ' + str(endhours) + ':' + (str(endminutes) if endminutes else '00') + endtimeofday
                drawblack.text((74, offset), text1, font = smallFont, fill = 0)
                offset += 18
                drawblack.text((74, offset), text2, font = smallFont, fill = 0)
            shiftIndex += 1
        drawblack.line((0, top, 378, top), fill = 0)
        drawblack.text((10, top + 5), calendar.day_name[currentDay.weekday()][0:3], font = mediumFont, fill = 0)
        drawblack.text((10, bottom - 50), str(currentDay.day), font = largeFont, fill = 0)
        currentDay = currentDay + timedelta(days = 1)
        i += 1
        
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5bc.epdconfig.module_exit()
    exit()
    

    
    
    
