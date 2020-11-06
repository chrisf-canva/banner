#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse
import datetime
import json

ANDROID = 'android'
IOS = 'ios'

ORIG_ACTION_2 = 'Action2'
ORIG_SEARCH_QUERY_2 = 'SearchQuery2'
ORIG_CAMPAIGN_NAME = 'campaign name'
ORIG_ONLINE_TIME = 'Online time'
ORIG_OFFLINE_TIME = 'Offline time'

DESCRIPTION = 'description'
DEEP_LINK = 'deepLink'
ACTION_2 = 'action2'
SEARCH_QUERY_2 = 'searchQuery2'
CAMPAIGN_NAME = 'campaignName'
BANNER_URL = 'bannerUrl'
MIN_TIME = 'minTime'
MAX_TIME = 'maxTime'


def read_banner(file_name, banner_url):
    data = {IOS: [], ANDROID: []}
    try:
        with open(file_name) as file:
            lines = file.readlines()
            new_node = True
            for i, line in enumerate(lines):
                # print(f'Line {i}: {line}')
                if line == '\n':
                    new_node = True
                elif new_node:
                    # if 'node_ios' in dir() and 'node_android' in dir():
                    #     format_description(node_ios)
                    #     format_description(node_android)
                    #     print(f'node_ios {i}: {node_ios}')
                    #     print(f'node_android {i}: {node_android}')
                    node_ios = {}
                    node_android = {}
                    data[IOS].append(node_ios)
                    data[ANDROID].append(node_android)
                    description = line.strip()
                    node_ios[DESCRIPTION] = description
                    node_android[DESCRIPTION] = description
                    node_ios[DEEP_LINK] = {}
                    node_android[DEEP_LINK] = {}
                    new_node = False
                else:
                    item = line.strip().split(':', 1)
                    key = map_key(item[0].strip())
                    append_value(key, item[1].strip(), node_ios, node_android, banner_url)
        # print(f'data: {data}')
        for i, node in enumerate(data[IOS]):
            format_description(node)
            print(f'node_ios {i}: {node}')
        for i, node in enumerate(data[ANDROID]):
            format_description(node)
            print(f'node_android {i}: {node}')
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()
    # print(data)
    return data


def save_banner(banner_dict, out_file):
    print(f'\n\n\n*******************\nsave banner to {out_file}\n')
    # print(f"\nbanner:\n{banner}\n\n\n\n\n\n")
    result = json.dumps(obj=banner_dict, indent=2, sort_keys=False)
    # print(f"\n\nNEW banner:\n{result}")
    try:
        with open(out_file, "w") as file:
            file.write(result)
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()


def format_description(node):
    time_stamp = ''
    if MIN_TIME in node and node[MIN_TIME]:
        time_stamp = ' from [%s]' % transform_millisecond_to_date_time_string(node[MIN_TIME])
        # print(f'time_stamp: {time_stamp}')
    if MAX_TIME in node and node[MAX_TIME]:
        time_stamp += ' to [%s]' % transform_millisecond_to_date_time_string(node[MAX_TIME])
        # print(f'time_stamp: {time_stamp}')
    if time_stamp:
        node[DESCRIPTION] += time_stamp


def map_key(key):
    if key == ORIG_ACTION_2:
        return ACTION_2
    elif key == ORIG_SEARCH_QUERY_2:
        return SEARCH_QUERY_2
    elif key.lower() == ORIG_CAMPAIGN_NAME:
        return CAMPAIGN_NAME
    elif key.lower() == ORIG_ONLINE_TIME.lower():
        return MIN_TIME
    elif key.lower() == ORIG_OFFLINE_TIME.lower():
        return MAX_TIME
    else:
        return key


def append_value(key, value, node_ios, node_android, banner_url):
    if key == CAMPAIGN_NAME:
        campaigns = value.rsplit('-', 1)
        campaign_prefix = campaigns[0]
        campaign_platforms = campaigns[1].split('/', 1)
        # print(f'campaign: {campaign_prefix} / {campaign_platforms}')
        for campaignPlatform in campaign_platforms:
            if campaignPlatform.lower() == IOS:
                campaign_name = campaign_prefix + '-' + campaignPlatform
                node_ios[CAMPAIGN_NAME] = campaign_name
                node_ios[BANNER_URL] = banner_url + campaign_name + '.png'
            elif campaignPlatform.lower() == ANDROID:
                campaign_name = campaign_prefix + '-' + campaignPlatform
                node_android[CAMPAIGN_NAME] = campaign_name
                node_android[BANNER_URL] = banner_url + campaign_name + '.png'
            else:
                raise (Exception("unknown campaign platform {campaignPlatform}"))
    elif key == MIN_TIME:
        date_time = transform_string_to_date_time(value)
        # print(f'minTime: {date_time}')
        node_ios[key] = date_time
        node_android[key] = date_time
    elif key == MAX_TIME:
        date_time = transform_string_to_date_time(value)
        # print(f'maxTime: {date_time}')
        node_ios[key] = date_time
        node_android[key] = date_time
    elif key == ACTION_2 or key == SEARCH_QUERY_2:
        node_ios[DEEP_LINK][key] = value.lower()
        node_android[DEEP_LINK][key] = value.lower()
    else:
        node_ios[key] = value
        node_android[key] = value


def transform_string_to_date_time(value):
    # 2020-01-05 09:00 AM
    return datetime.datetime.strptime(value, '%Y-%m-%d %I:%M %p').timestamp() * 1000


def transform_millisecond_to_date_time_string(value):
    # 2020-01-05 09:00 AM
    return datetime.datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %I:%M %p')


parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--banner', '-b', help='banner info file 属性，必要参数', required=True)
parser.add_argument('--bannerUrl', '-burl', help='banner URL file 属性，必要参数', required=True)
parser.add_argument('--out', '-o', help='output json file 属性，非必要参数', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    banner = args.banner
    bannerUrl = args.bannerUrl
    out = args.out or '%s_after.json' % banner
    print(f"""
        banner file: {banner}
        bannerUrl file: {bannerUrl}
        out file: {out}
    """)
    banner = read_banner(banner, bannerUrl)
    save_banner(banner, out)
