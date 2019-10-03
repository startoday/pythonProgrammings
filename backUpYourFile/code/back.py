#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time



source = ["/Users/zoeyw/Documents/backUpYourFile/test/","/Users/zoeyw/Documents/backUpYourFile/test2/"]
target_dir = "/Users/zoeyw/Documents/backUpYourFile/storage/"

today_dir = target_dir + time.strftime('%Y%m%d')
time_dir = time.strftime('%H:%M') + 'backup'


#-q means work quietky,
#-r means work recursively

#' '.join(source) change the source into string
touch = today_dir + os.sep + time_dir + '.zip'
cmd_touch = "zip -qr " + touch +' '+ ' '.join(source)


#zip_command = "zip -qr %s %s" %(target, ' '.join(source))


if os.path.exists(today_dir)==0:
    os.mkdir(today_dir)
if os.system(cmd_touch) == 0:
    print("Successful backup")
else :
    print("Backup Failed")


