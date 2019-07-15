import time
from datetime import *
import re
####
# 将时间统一转化为 2018-07-23 15:07:21
####
# a = float(1532329641)
# t = datetime.fromtimestamp(a) # 2018-07-23 15:07:21
# print(t)
# result = re.match(r'^[\d]+$', "1532329641")
# if result:
#     print(1)
# else:
#     print(2)
# print(result)

# string = "123 907"
# result = string.split(" ")
# print(result[1])

# string = "5分钟前"
# back = re.search(r'[\d]+', string)
# result = datetime.now()-timedelta(minutes=int(back.group()))
# print(str(result.date())+" "+str(result.time())[:8])

# string = "昨天 15:26"
# back = re.search(r'\d{2}:\d{2}', string)
# yesterday = datetime.now()-timedelta(hours=24)
# print(str(yesterday.date()) + " " + str(back.group()) + ":00")


def timestamp(string):
    return re.match(r'^[\d]+$', string)


def standard_time(string):
    return re.match(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$', string)


def miss_time(string):
    return re.match(r'^\d{4}-\d{2}-\d{2}$', string)


def miss_year(string):
    return re.match(r'^\d{2}-\d{2}$', string)


def second_front(string):
    return re.match(r'^\d+分钟前$', string)


def hour_front(string):
    return re.match(r'^\d+小时前$', string)


def yesterday_(string):
    return re.match(r'^昨天\s\d{2}:\d{2}$', string)


def miss_zero(string):
    if re.match(r'^\d{4}-\d-\d{2}$', string):
        return True
    elif re.match(r'^\d{4}-\d{2}-\d$',string):
        return True
    elif re.match(r'^\d{4}-\d-\d$',string):
        return True
    else:
        return False

# string = "昨天 19:09"
def deal_time(string):
    if string is None:
        return None
    elif standard_time(string):
        # print("标准时间")
        return string
    elif timestamp(string):
        return datetime.fromtimestamp(float(string))
    elif miss_time(string):
        return string+" 00:00:00"
    elif miss_year(string):
        year = datetime.now().year
        return str(year)+"-"+string+" 00:00:00"
    elif second_front(string):
        back = re.search(r'[\d]+', string)
        result = datetime.now() - timedelta(minutes=int(back.group()))
        return str(result.date()) + " " + str(result.time())[:8]
    elif hour_front(string):
        back = re.search(r'[\d]+', string)
        result = datetime.now() - timedelta(hours=int(back.group()))
        return str(result.date()) + " " + str(result.time())[:8]
    elif yesterday_(string):
        back = re.search(r'\d{2}:\d{2}', string)
        yesterday = datetime.now()-timedelta(hours=24)
        return str(yesterday.date()) + " " + str(back.group()) + ":00"
    elif miss_zero(string):
        li = string.split('-')
        if re.match(r'^\d{4}-\d-\d{2}$', string):
            return li[0]+'-'+'0'+li[1]+'-'+li[2]+' 00:00:00'
        elif re.match(r'^\d{4}-\d{2}-\d$',string):
            return li[0]+'-'+li[1]+'-'+'0'+li[2]+' 00:00:00'
        elif re.match(r'^\d{4}-\d-\d$',string):
            return li[0]+'-'+'0'+li[1]+'-'+'0'+li[2]+' 00:00:00'
# b = time.time()
# print(type(b))


if __name__ == '__main__':
    string = '1563118670'
    result = deal_time(string)
    print(result)
