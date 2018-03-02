import gspread
import time, datetime
import random
import sys, subprocess
from oauth2client.service_account import ServiceAccountCredentials

#for the gspread and authentication
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('mycreds.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Lab2GSheet").sheet1

wks.resize(1) #resize the whole spread sheet to one so append works

p_start = time.time()#get the start time
post_f = False #post flag
post_time = p_start

while(True):
    p_current = time.time() #get the current time
    test_time = (int(p_current) -int(post_time))%30
    current_time = str(datetime.datetime.now()) #.microsecond#get the current time
    
    if (post_f == True) and (test_time == 0): #if something is post in 30 secs
        post_f = False #reset the flag
        test_time=1
    
    rand_num1 = random.randint(0, 100000) #get a random number
    random.seed(time.time()) #change the seed
    rand_num2 = random.randint(0,100000) #get another random number

    if (rand_num1 == rand_num2): #if the random number picked equals to the time range
        post_f = True #set the flag
        post_time = time.time()
        result = subprocess.check_output('fortune') #run the fortune command and output to result
        wks.append_row([current_time, result]) #append it to the end of the file
        print('Posted 1')

    if (post_f == False) and (test_time == 0): #if noting is post in 30 secs
        post_f = True #set the flag
        test_time = 1
        post_time = time.time()
        result = subprocess.check_output('fortune') #run the fortune command and output to result
        wks.append_row([current_time,result]) #append it to the end of the file
        print('Posted 2')

    p_end = time.time() #get the end time
    if(int(p_end - p_start) == 180): #at 3 mins
        sys.exit() #exit program