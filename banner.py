#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse
import re
import json
import datetime

def readBanner(fileName, bannerUrl):
	data = {}
	data['ios']= []
	data['android'] = []
	try:
		with open(fileName) as file:
			lines = file.readlines()
			nodeIOS = {}
			nodeAndroid = {}
			newNode = True
			for i, line in enumerate(lines):
				# print(f'Line {i}: {line}')
				if line == '\n':
					newNode = True
				elif newNode:
					print(f'nodeIOS {i}: {nodeIOS}')
					print(f'nodeAndroid {i}: {nodeAndroid}')
					nodeIOS = {}
					nodeAndroid = {}
					data['ios'].append(nodeIOS)
					data['android'].append(nodeAndroid)
					description = line.strip()
					nodeIOS['description'] = description
					nodeAndroid['description'] = description
					nodeIOS['deepLink'] = {}
					nodeAndroid['deepLink'] = {}
					newNode = False
				else:
					item = line.strip().split(':', 1)
					key = mapKey(item[0].strip())
					appendValue(key, item[1].strip(), nodeIOS, nodeAndroid, bannerUrl)
			# print(f'data: {data}')
	except Exception as e:
		print(e)
		raise
	finally:
		file.close()
	# print(data)
	return data	

def saveBanner(banner, out):
    print(f'\n\n\n*******************\nsave banner to {out}\n')
    # print(f"\nbanner:\n{banner}\n\n\n\n\n\n")
    result = json.dumps(banner, indent=2, sort_keys=False)
    # print(f"\n\nNEW banner:\n{result}")
    try:
        with open(out, "w") as file:
            file.write(result)
    except Exception as e:
        print(e)
        raise
    finally:
        file.close()	

def mapKey(key):
	if key == 'Action2':
		return 'action2'
	elif key == 'SearchQuery2':
		return 'searchQuery2'
	elif key.lower() == 'campaign name':
		return 'campaignName'
	elif key.lower() == 'Online time'.lower():
		return 'minTime'
	elif key.lower() == 'Offline time'.lower():
		return 'maxTime'
	else:
		return key

def appendValue(key, value, nodeIOS, nodeAndroid, bannerUrl):
	if key == 'campaignName':
		campaigns = value.rsplit('-', 1)
		campaignPrefix = campaigns[0]
		campaignPlatforms = campaigns[1].split('/', 1)
		for campaignPlatform in campaignPlatforms:
			if campaignPlatform.lower() == "ios":
				campaignName = campaignPrefix + '-' + campaignPlatform
				nodeIOS['campaignName'] = campaignName
				nodeIOS['bannerUrl'] = bannerUrl + campaignName + '.png'
			elif campaignPlatform.lower() == "android":
				campaignName = campaignPrefix + '-' + campaignPlatform
				nodeAndroid['campaignName'] = campaignName
				nodeAndroid['bannerUrl'] = bannerUrl + campaignName + '.png'
			else:
				raise(Exception("unknown campaign platform {campaignPlatform}"))
	elif key == 'minTime':
		dateTime = mapDateTime(value)
		print("minTime: {dateTime}")
		nodeIOS[key] = dateTime
		nodeAndroid[key] = dateTime
	elif key == 'maxTime':
		dateTime = mapDateTime(value)
		print("maxTime: {dateTime}")
		nodeIOS[key] = dateTime
		nodeAndroid[key] = dateTime
	elif key == 'action2' or key == 'searchQuery2':
		nodeIOS['deepLink'][key] = value.lower()
		nodeAndroid['deepLink'][key] = value.lower()
	else:
		nodeIOS[key] = value
		nodeAndroid[key] = value

def mapDateTime(value):
	# 2020-01-05 09:00 AM
	return datetime.datetime.strptime(value, '%Y-%m-%d %I:%M %p').timestamp() * 1000

parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--banner', '-b', help='banner info file 属性，必要参数', required=True)
parser.add_argument('--bannerUrl', '-burl', help='banner URL file 属性，必要参数', required=True)
parser.add_argument('--out', '-o', help='output json file 属性，非必要参数', required=False)
args = parser.parse_args()

if __name__ == '__main__':
	banner = args.banner
	bannerUrl = args.bannerUrl
	out = args.out or banner + '_after.json'
	print(f"""
		banner file: {banner}
		bannerUrl file: {bannerUrl}
		out file: {out}
		"""
	)
	banner = readBanner(banner, bannerUrl)
	saveBanner(banner, out)