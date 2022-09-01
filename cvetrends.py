# -*- coding: utf-8 -*-
"""
Author: psjs97 (https://github.com/psjs97)
"""

# Libraries
import argparse
import xmltodict
import re, os, requests
from datetime import datetime

# Arguments
parser = argparse.ArgumentParser(description='Trending CVEs script: get last trending CVEs from @CVEtrends Twitter account.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument("-t", "--today", action="store_true", help="Trending CVEs from last 24 hours")
#parser.add_argument("-w", "--week", action="store_true", help="Trending CVEs from last week")
args = parser.parse_args()



rss_feed_url = 'https://nitter.net/CVEtrends/rss'

def get_current_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Script execution datetime: ", dt_string)	

def banner():
    # Script banner
    os.system('color')
    print('\033[92m' + '\033[01m' + """
    
     /$$$$$$$$                                  /$$ /$$                            /$$$$$$  /$$    /$$ /$$$$$$$$          
    |__  $$__/                                 | $$|__/                           /$$__  $$| $$   | $$| $$_____/          
       | $$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$ /$$ /$$$$$$$   /$$$$$$       | $$  \__/| $$   | $$| $$        /$$$$$$$
       | $$ /$$__  $$ /$$__  $$| $$__  $$ /$$__  $$| $$| $$__  $$ /$$__  $$      | $$      |  $$ / $$/| $$$$$    /$$_____/
       | $$| $$  \__/| $$$$$$$$| $$  \ $$| $$  | $$| $$| $$  \ $$| $$  \ $$      | $$       \  $$ $$/ | $$__/   |  $$$$$$ 
       | $$| $$      | $$_____/| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$      | $$    $$  \  $$$/  | $$       \____  $$
       | $$| $$      |  $$$$$$$| $$  | $$|  $$$$$$$| $$| $$  | $$|  $$$$$$$      |  $$$$$$/   \  $/   | $$$$$$$$ /$$$$$$$/
       |__/|__/       \_______/|__/  |__/ \_______/|__/|__/  |__/ \____  $$       \______/     \_/    |________/|_______/ 
                                                                  /$$  \ $$                                               
                                                                 |  $$$$$$/                                               
                                                                  \______/                                                
    """ + '\033[0m')
    print('\033[93m' + '\033[01m' +"[ Author: psjs97 ] | https://github.com/psjs97\n" + '\033[0m')

    
def get_rss_feed(rss_url = rss_feed_url):
    try:
        response = requests.get(rss_feed_url)
        if response.status_code != 200:
            raise SystemExit("Http response code: {code}. Not possible to fetch rss feed.".format(code=str(response.status_code)))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    
    rss_feed_xml = xmltodict.parse(response.text)
    return rss_feed_xml

def preprocess_xml(rss_feed_xml):
    tweet_msg = rss_feed_xml['rss']['channel']['item'][0]['title']
    
    tweet_lines_list = tweet_msg.split('\n')
    tweet_dict = {}
    
    current_key = ''
    for line in tweet_lines_list:
        if line.lower().startswith('past') and line not in tweet_dict.keys():
            tweet_dict[line] = []
            current_key = line
        if line.lower().startswith('cve'):
            cve = re.findall(r'cve-\d{4}-\d{3,7}', line.lower())[0].upper()
            cve_audience = line.lower().split(': ')[-1].split(' ')[0].upper()
            cve_tuple = (cve, cve_audience)
            tweet_dict[current_key].append(cve_tuple)

    return tweet_dict

def main():
    banner()
    get_current_datetime()
    rss_feed_xml = get_rss_feed()
    tweet_dict = preprocess_xml(rss_feed_xml)
    print()
    for key in tweet_dict.keys():
        print('- ' + key)
        for cve in tweet_dict[key]:
            print('\t' + cve[0] + ' -> ' + cve[1] + ' audience')
    
if __name__=='__main__':
    main()
    
    
    
    
    
    
    
    
    
    