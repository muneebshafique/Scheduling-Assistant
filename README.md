# Scheduling-Assistant

Description:
This program allows a user to manage his weekly tasks in an Organized Manner.

Current Features:
Timetable= This allows the user to view his weekly events sorted in a well-formatted Table.
Reminders= This allowes the user to view his weekly reminders in a sorted well-formatted Table.

The input for these 2 features is managed by a csv file called Schedule.csv. Save the schedule and proceed to [Daily Use](
Input your schedule into schedule.csv
Required Fields:

Event Name- The name you refer to your meeting as (ex. HIST101, Gym, etc.).
Event Days- The days your recurring meeting is on (ex. MWR is Monday, Wednesday, Thursday of each week).
M = Monday
T = Tuesday
W = Wednesday
R = Thursday
F = Friday
S = Saturday
U = Sunday
Event Start Time- The time your meeting starts (uses the 24-hour format. HH-MM).
Event End Time- The time your meeting ends (uses the 24-hour format. HH-MM).
Category: At the moment all tasks must be classfied into 3 categories i.e. (Work,Leisure,Hobbies)


Free Time Slots=This allows the user to see which time slots are free for every day in the week. Any time slot that is greater than 30 min is viewable. Again the output is in a sorted table format.

3 Productivity Graphs
Daily Productivity: Automatically produces a bar graph which shows the hours spent doing some taks. This includes all 3 categories of work done per day.
Time Journal: Automatically produces a bar graph which shows the hours spent doing tasks classified as work per week.
Pie chart: Gives a holistic view of how time was spent on each of the 3 categories per week.

Clashes:
The program will automatically detect any clashes if any from the data in the csv file. It will also dsiplay possible options where the task might be put. In this case the Timetable and free time slots will not be generated. The program will wait for you to change the entry in the csv file and save it.

Motivational Quotes
The program will output an inspiring quote every time it is run to boost productivity. This is selected from the file motivational.txt.

Automatic Rescheduler:
Sometimes one is not able to complete all tasks he ought to complete in one day. This program provides an easy way for you to reschdule tasks of that day.
The program stores current day. Task number must be inputted first which signifies the task that is to be rescheduled.
Pressing the options button will provide a list of options where the task can be rescheduled.
You may select the option where you want to reschedule the task.
You may now clear the screen by pressing the clear button.
Now press the submit button to  reschedule the task. This will also make changes to the csv file(Schedule).
HAPPY  RESCHEDULING!



GETTING STARTED;
To get the Schedule Assistant; follow the steps below.

Prerequisites;
Download and install Python Version 3.8.X or newer

INSTALLATION:
Install pip Packages
pip install matplotlib
pip install tkinter


