# -*- coding: utf-8 -*-

'''
------------------------------------------------
           Canvas TODO Notifier v1.0
                By Jordan Hillis
            contact@jordanhillis.com
            http://jordanhillis.com
 ------------------------------------------------

MIT License

Copyright (c) 2017 Jordan S. Hillis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time, os, calendar, requests, sys
from time import sleep
from datetime import date, datetime, timedelta
from selenium import webdriver
from itertools import repeat
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from pushover import Client

# UTF8 encoding
reload(sys)
sys.setdefaultencoding('utf8')

'''
*********************
***** SETTINGS ******
*********************
'''
username = "john.smith"                                 # Username for Canvas
password = "password123"                                # Password for Canvas
school = "champlain"                                    # School for Canvas
pushover_user_key = "u2dfavf788ab4qteakhivx3993hg14"    # Pushover user key
pushover_api_key = "a5gaqf9dvoiiq6ey5t8at6w99ocv5x"     # Pushover app api key
version="1.0"						# Version
display_x = 1200					# Screen X size
display_y = 800						# Screen Y size
geckodriver = "/usr/local/bin/geckodriver"		# Geckodriver location


# Header
print("\033[91m\033[1m")
print("------------------------------------------------")
print("          Canvas TODO Notifier v"+version)
print("               By Jordan Hillis")
print("           contact@jordanhillis.com")
print("           http://jordanhillis.com")
print("------------------------------------------------")
print("\033[0m")

# Create display
display = Display(visible=0, size=(display_x, display_y))
display.start()

# Web driver configuration and execute driver
firefox_profile = webdriver.FirefoxProfile()
# Disable images/flash and set browser to Safari on MacOS
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
firefox_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.43 (KHTML, like Gecko) Version/10.0 Safari/602.1.43")
browser = webdriver.Firefox(executable_path = geckodriver, firefox_profile=firefox_profile)
browser.set_page_load_timeout(30)

# Determine greeting that will be used for notifications
current_hour = int(time.strftime('%H:%M').split(':')[0])
if current_hour >= 5 and current_hour <= 11:
    greeting = "Good morning"
elif current_hour >= 12 and current_hour <= 17:
    greeting = "Good afternoon"
elif current_hour >= 18 or current_hour <= 4:
    greeting = "Good evening"

# Notifications function using pushover to notify
def notify_me(notify_msg,notify_title):
	global pushover_user_key, pushover_api_key
	client = Client(pushover_user_key, api_token=pushover_api_key)
	client.send_message(notify_msg, title=notify_title)

# Login to Canvas and grab my name
def canvas_login():
	global my_name
	print("[" + time.strftime("%H:%M:%S") + "] [-] Loading "+str(school).title()+" Canvas...")
	# Load school Canvas page
	browser.get('https://'+str(school)+'.instructure.com/')
	print("[" + time.strftime("%H:%M:%S") + "] [-] Waiting 10 seconds...")
	sleep(10)
	# Select 2nd login method on schools authetication options
	print("[" + time.strftime("%H:%M:%S") + "] [-] Clicking on the 2nd login option...")
	browser.find_element_by_xpath("(//tr[@class='clickable-row'])[2]").click()
	print("[" + time.strftime("%H:%M:%S") + "] [-] Waiting 15 seconds...")
	sleep(15)
	# Attempt to login using username and password
	try:
		print("[" + time.strftime("%H:%M:%S") + "] [-] Logging into "+str(school).title()+" Canvas...")
		print("[" + time.strftime("%H:%M:%S") + "] [-] Typing in username and password.")
		user_name = browser.find_element_by_xpath("//input[@name='username']")
		pass_word = browser.find_element_by_xpath("//input[@name='password']")
		user_name.send_keys(username)
		pass_word.send_keys(password)
		sleep(2)
		pass_word.send_keys(Keys.RETURN)
		print("[" + time.strftime("%H:%M:%S") + "] [-] Submitting login information.")
		print("[" + time.strftime("%H:%M:%S") + "] [-] Waiting 15 seconds...")
		sleep(15)
		try:
			if browser.find_element_by_xpath("//input[@name='username']").is_displayed():
				notify_me("Unable to login to Canvas using the username and password stored.",str(school).title()+" Canvas Notification")
				print("[" + time.strftime("%H:%M:%S") + "] [*] Username/password did not login successfully.")
				browser.quit()
				display.stop()
				exit()
		except Exception:
			pass
	# Notify if any errors occur during the login that aren't wrong username/password based
	except Exception:
		pass
		notify_me("Something went wrong while trying to login to Canvas.",str(school).title()+" Canvas Notification")
		print("[" + time.strftime("%H:%M:%S") + "] [*] Something has gone wrong...")
		browser.quit()
		display.stop()
		exit()
	# We are logged in, grab name used on Canvas
	my_name = browser.find_element_by_xpath("//img").get_attribute("alt")
	print("[" + time.strftime("%H:%M:%S") + "] [*] Successfully logged in as '" + str(my_name.upper()) + "'")
	return my_name

# Grab TODO list and notify
def notify_todo():
	global my_name
	# Set blank variable for todo_msg
	todo_msg = ""
	# Check if we are truly logged in
	if my_name != "":
		print("[" + time.strftime("%H:%M:%S") + "] [-] Generating TODO notification data...")
		# Check if there is more todos in the full list and if so click on the more option
		try:
			if browser.find_element_by_xpath("//a[@class='more_link']").is_displayed():
				browser.find_element_by_xpath("//a[@class='more_link']").click()
				sleep(3)
		except Exception:
			pass
		# Loop through each todo and append it to the todo_msg
		for todos in browser.find_elements_by_xpath("//li[@class='todo']"):
			# Gather task title, class title, due date, and what type of task it is
			task_title = todos.find_element_by_xpath('.//b[@class="todo-details__title"]').text
			task_class = todos.find_element_by_xpath('.//p[@class="todo-details__context"]').text
			task_due = todos.find_element_by_xpath("(.//p)[2]").text
			task_type = todos.find_element_by_xpath(".//i").get_attribute("aria-label")
			# Check if task_title is blank or is worth 0 points, if so dont add it to the final message, if not append it
			if task_title != "" and task_due.startswith("0 points") == False and task_due[0].isdigit():
				todo_msg += "["+str(task_class)+"] ["+str(task_type)+"]\n"+str(task_title)+"\n"+str(task_due)+"\n\n"
		# Check if there is even any tasks added, if not tell us we are complete for the day
		if todo_msg == "":
			notify_me(str(greeting)+" "+str(my_name)+",\n\nLooks like you have no tasks to complete for the day! :D",str(school.title())+" TODO Notification")
			print("\nLooks like you have no tasks to complete for the day! :D")
			file = open("todo_tasks.txt","w") 
			file.write(str(my_name)+" it looks like you have no tasks to complete for the day!") 
			file.close()
		# Notify with a full list of all the TODOS
		else:
			notify_me(str(greeting)+" "+str(my_name)+",\n\nToday you need to complete the following...\n\n"+str(todo_msg), str(school.title())+" TODO Notification")
			print("\nToday you need to complete the following:\n---------------------------------------------\n\n"+str(todo_msg)+"---------------------------------------------")
			file = open("todo_tasks.txt","w") 
			file.write(str(my_name)+" today you need to complete the following "+str(todo_msg)) 
			file.close()

# Login to Canvas
canvas_login()

# Grab todo and notify via email or pushover
notify_todo()

# Stop browser, display and quit script
browser.quit()
display.stop()
