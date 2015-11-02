#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, date
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
