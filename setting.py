#POST to The hezong website
#page 3

import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import time
import json
from datetime import date
import datetime

from termcolor import colored

with open('commu.json') as json_data_file:
    conf = json.load(json_data_file)


user = 'Admin'
password = 'Admin0000'

switch = 1
capacity = 2
start_time = [0,0,0,0,0,0,0]
end_time = [0,0,0,0,0,0,0]

def POST(ip, switch, start_time, end_time):
    
    url = 'http://'+ip+'/protect/power1.htm'

    login = HTTPBasicAuth(user,password)

    res = requests.get(url, auth=login)
    soup_res = BeautifulSoup(res.text,'html.parser')
    timebox = soup_res.find(attrs={'name':'textfield20'}).attrs['value']
    time_string = datetime.datetime.now().strftime("%H:%M")
    print("Now : ",time_string,)
    
    '''
    ====== Read ======
    radio20     : SavingMode(0:off; 1:on)
    textfield20 : Time
    select0     : Capacity(0:full; 1:half; 2:smart)
    select3     : Day

    ====== Write ======
    textfield21 : Mon_start
    textfield22 : Tues_start
    textfield23 : Wed_start
    textfield24 : Thr_start
    textfield25 : Fri_start
    textfield26 : Sat_start
    textfield27 : Sun_start

    textfield28 : Mon_end
    textfield29 : Tues_end
    textfield30 : Wed_end
    textfield31 : Thr_end
    textfield32 : Fri_end
    textfield33 : Sat_end
    textfield34 : Sun_end

    '''

    payloadd = {'radio20':switch,'select0':capacity,'textfield21':start_time[0],'textfield28':end_time[0],
    'textfield22':start_time[1],'textfield29':end_time[1],
    'textfield23':start_time[2],'textfield30':end_time[2],'seclect3':1,
    'textfield24':start_time[3],'textfield31':end_time[3],
    'textfield25':start_time[4],'textfield32':end_time[4],'textfield20':time_string,
    'textfield26':start_time[5],'textfield33':end_time[5],
    'textfield27':start_time[6],'textfield34':end_time[6]}
    # print(colored(payloadd,'blue'))
    try:
        time.sleep(1)
        print(colored("setting...",'green'))
        res_post = requests.post(url, data=payloadd, auth=login)
        # print(colored("Response POST:",res_post.status_code),'yellow')
        print("Response POST:",res_post.status_code)
        # print("try")
    except Exception as ex:
        print('message":"error for '+str(ex))

def UPDATE(ip,start,end):
    print(colored("loading...",'green'))
    url = 'http://'+ip+'/protect/power1.htm'
    try:
        login = HTTPBasicAuth(user, password)
        
        res = requests.get(url, auth=login)
        soup = BeautifulSoup(res.text,'html.parser')

        switch = int(soup.find('input',attrs={'name':'radio20'}).has_attr('checked'))
        capacity = int(soup.find('select',attrs={'name':'select0'}).find_all('option', selected = True)[0]['value'])
        start_time[0] = (soup.find(attrs={'name':'textfield21'}).attrs['value']).encode('ascii','igore')
        end_time[0] = (soup.find(attrs={'name':'textfield28'}).attrs['value']).encode('ascii','igore')
        start_time[1] = (soup.find(attrs={'name':'textfield22'}).attrs['value']).encode('ascii','igore')
        end_time[1] = (soup.find(attrs={'name':'textfield29'}).attrs['value']).encode('ascii','igore')
        start_time[2] = (soup.find(attrs={'name':'textfield23'}).attrs['value']).encode('ascii','igore')
        end_time[2] = (soup.find(attrs={'name':'textfield30'}).attrs['value']).encode('ascii','igore')
        start_time[3] = (soup.find(attrs={'name':'textfield24'}).attrs['value']).encode('ascii','igore')
        end_time[3] = (soup.find(attrs={'name':'textfield31'}).attrs['value']).encode('ascii','igore')
        start_time[4] = (soup.find(attrs={'name':'textfield25'}).attrs['value']).encode('ascii','igore')
        end_time[4] = (soup.find(attrs={'name':'textfield32'}).attrs['value']).encode('ascii','igore')
        start_time[5] = (soup.find(attrs={'name':'textfield26'}).attrs['value']).encode('ascii','igore')
        end_time[5] = (soup.find(attrs={'name':'textfield33'}).attrs['value']).encode('ascii','igore')
        start_time[6] = (soup.find(attrs={'name':'textfield27'}).attrs['value']).encode('ascii','igore')
        end_time[6] = (soup.find(attrs={'name':'textfield34'}).attrs['value']).encode('ascii','igore')
        
        ## Modify the weekday
        weekday = week()
        start_time[weekday] = start 
        end_time[weekday] = end

        result_data = {
            "switch": switch,
            "capacity": capacity,
            "Mon_start": start_time[0],
            "Mon_end": end_time[0],
            "Tues_start": start_time[1],
            "Tues_end": end_time[1],
            "Wed_start": start_time[2],
            "Wed_end": end_time[2],
            "Thr_start": start_time[3],
            "Thr_end": end_time[3],
            "Fri_start": start_time[4],
            "Fri_end": end_time[4],
            "Sat_start": start_time[5],
            "Sat_end": end_time[5],
            "Sun_start": start_time[6],
            "Sun_end": end_time[6]
        }
        # print(result_data)

    except Exception as ex:
        print(ex)

def week():
    weekday = datetime.datetime.today().weekday() #int
    #Mon to Sun = 0 to 6
    return weekday

def SELECT(Device_ID):
    for i in range(len(conf)):
        if(conf[i]['Device_ID'] == Device_ID):
            return conf[i]["IP"]

def run(device_input,start_input,end_input):
    IP = SELECT(device_input)
    UPDATE(IP,start_input,end_input)
    # print(start_time,end_time)
    POST(IP,switch,start_time,end_time)

#print(colored("[Building]_[Floor]_[Number]",'yellow'))
#device_input = input("Device ID : ")
#print(colored("[HOUR]:[MIN]",'yellow'))
#start_input = input("Start Time : ")
#print(colored("[HOUR]:[MIN]",'yellow'))
#end_input = input("End Time : ")

if __name__ == '__main__':
    run(device_input,start_input,end_input)
