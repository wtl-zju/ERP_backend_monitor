__author__ = 'TianluWang'
from config import time_node, requests
from json_body_makeup import json_body_makeup
from datetime import datetime, timedelta
from open_app import ip_location
import re


def request_info(files):

    json_bodys = []
    pre_time = str(time_node)[:-7].replace(" ", "T")

    for file in files:
        with open(file) as f:
            for line in f.readlines():
                line_list = line.split(' ')
                if line_list[3][1:-7] < pre_time:
                    continue
                url = line_list[5]
                if '/bc/' not in url:
                    continue
                match = re.match(r'(.*)\d', url)
                if match is not None:  # remove random number sequence in the url
                    url_reverse = url[::-1]
                    pos = url_reverse.index('/')
                    url = url[:-(pos+1)]
                if url in requests:
                    url_split = url.split('/')
                    measurement = url_split[-2]+'_'+url_split[-1]  # make up the measurement name from the end of url
                    CST_time_s = line_list[3][1:-7].replace("T", " ")
                    CST_time = datetime.strptime(CST_time_s, '%Y-%m-%d %H:%M:%S')
                    UTC_time = CST_time - timedelta(hours=8)
                    time = str(UTC_time).replace(" ", "T")
                    value = {}
                    value['ip'] = line_list[0]
                    value['country'] = ip_location(value['ip'])
                    value['status'] = line_list[7]
                    value['time_cost_new'] = float(line_list[-3])
                    value['Android'] = 'Android' in line
                    value['iPhone'] = 'iPhone' in line
                    if 'Android' in line:
                        value['an_or_ios'] = '1'
                    else:
                        value['an_or_ios'] = '0'
                    value['url'] = line_list[5]
                    json_body = json_body_makeup(measurement, time, value)
                    json_bodys.append(json_body)

    return json_bodys
