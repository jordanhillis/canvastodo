![LAU Logo](https://jordanhillis.com/images/github/ctn/logo.png)

This program automates a login into your Canvas Learning Management System account and grabs your current TODO list and notifies you via push notification of the tasks you need to complete.

### Why was this created?

I am currently a Cyber Security student Champlain College and utilize the Canvas Learning Management System daily for my online classes. I wanted a way to be notified each morning when I wake up with the tasks that still need to be completed for my classes. Canvas did not have such feature, so instead I turned to creating my own program to do this task and made it automated to run each morning before I wake up.

## Features

* Logs in to Canvas LMS
* Grabs current TODO list
* Notifies via push notification (using Pushover)

## Example TODO Notification

![Home screen of Phone](https://jordanhillis.com/images/github/ctn/home.jpg)
![Pushover notification example](https://jordanhillis.com/images/github/ctn/notify.jpg)

## Latest Version

* v1.0

## Prerequisites

This program has been made for Linux users in mind. This will run on Windows, but you will have to change quite a few things for it to run properly.

* Firefox will need to be installed along with the geckodriver [(geckodriver download)](https://github.com/mozilla/geckodriver/releases)
* You will need to have a Pushover account (this is how it will send you push notifications to your device) https://pushover.net/
* Additionally you will need to have Python 3 installed on your system as well as the following python modules installed:
* * python-pushover
* * pyvirtualdisplay
* * selenium

The easiest way to install the required modules is to use PIP

##### PIP Install Command:

```
pip3 install python-pushover pyvirtualdisplay selenium
```

## Installing

To install Canvas TODO Notifier please enter the following command:

```
git clone https://github.com/jordanhillis/canvastodo.git
cd canvastodo
```

## Usage

Open the canvastodo folder and edit the 'canvastodo.py' file. Change the settings for your username, password, and school on canvas. Your Pushover user key and api key will also need to match your account information from Pushover.

Example:
```
'''
*********************
***** SETTINGS ******
*********************
'''
username = "john.smith"                               # Username for Canvas
password = "password123"                              # Password for Canvas
school = "champlain"                                  # School for Canvas
pushover_user_key = "u2dfavf788ab4qteakhivx3993hg14"  # Pushover user key
pushover_api_key = "a5gaqf9dvoiiq6ey5t8at6w99ocv5x"   # Pushover app api key
```
Save the file.

To run please enter the following command in the canvastodo folder:
```
python3 canvastodo.py
```

## Automating Canvas TODO Notifier

To automate this task and notify you each morning I recommend installing cron or a similiar service on your computer or server.

Using cron enter the following command:
```
crontab -e
```
Once your cron file is open enter the following and change the hour and path:
```
0 [HOUR] * * * python3 [PATH/TO/FOLDER]/canvastodo.py #Get canvas todo list
```
You will need to change [HOUR] to the hour in which you want to be notified, (ex: 6) and change the [PATH/TO/FOLDER] with the path to where you have installed this program (ex: /home/jordan/canvastodo)

Save the file and you are now ready to receive automatic notifications with your current Canvas TODO list.

## Developers

* **[Jordan Hillis](https://jordanhillis.com)** - *Lead Developer*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This program is not an official program by Canvas LMS or any affiliated school.
