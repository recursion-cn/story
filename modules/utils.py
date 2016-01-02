#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, date
import time
import json

# custom encode function for dateime and date type
class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return obj

# 把时间转换为距今时间表示，如“刚刚”，“一小时以前”，“昨天”，“一个月以前”
def date_distance(timestamp):
    target = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    delta = (now - target)
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return '刚刚'
    minutes = seconds / 60
    if minutes < 60:
        return str(minutes) + '分钟之前'
    hours = seconds / (60 * 60)
    if hours < 24:
        return str(hours) + '小时之前'
    days = seconds / (60 * 60 * 24)
    if days < 30:
        return str(days) + '天之前'
    months = seconds / (60 * 60 * 24 * 30)
    if months < 12:
        return str(months) + '月之前'
    return '===='
