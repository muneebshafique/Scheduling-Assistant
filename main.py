import csv
import schedule
import time
from datetime import date
from datetime import datetime, time
from datetime import datetime, timedelta
import datetime as dt
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, mainloop, LEFT, TOP
from tkinter.ttk import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk



def readcsv(filename):
    a="True"
    data=[]
    Reminders=[]
    #function extracts data from the excel file
    with open(filename, 'r') as file:
        reader=csv.reader(file)
        for row in reader:
            if row[1]!="" and a =="True":
                data.append(row)
            elif row[1]=="":
                a="False"
            elif a=="False":
                Reminders.append(row)
    #Picks first block as the main data
    #The second block as the reminders
    #Heading refers to the first row of the main block(evene, repeat,start...)

    Heading=data.pop(0)
    return (data, Heading,Reminders)

def Organize(Data):
    #setting up the basic dictionary with days of the week
    Table ={}
    Days_of_the_week=["MONDAY","TUESDAY","WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    for day in Days_of_the_week:
        Table[day]=[]


    for i in range(len(Data)):
        for j in range(len(Data[i])):
            #stopping at the second column where user has entered the days
            if j==1:
                #calling function to convert (MT)-->[MONDAY,TUESDAY]
                #Repeat is a list containing full form of days entered by user(repition days)
                Repeat=convert_days_to_fullform(Data[i][j])
                for day in Repeat:
                    day=day.upper()
                     #appending event,start time,end time
                    Table[day].append([Data[i][0],Data[i][2],Data[i][3],Data[i][4]])
    #gives a dictionary containing the main data
    return(Table)

def convert_days_to_fullform(days):
     #function converts convert (MT)-->[MONDAY,TUESDAY]
    DAY=[]
    map_days = {'M': ('Monday'),
                'T': ('Tuesday'),
                'W': ('Wednesday'),
                'R': ('Thursday'),
                'F': ('Friday'),
                'S': ('Saturday'),
                'U': ('Sunday')}
    days=days.upper()
    day=days.split()
    for i in day:
        DAY.append(map_days[i])
    return(DAY)

def Date_Today(today=0):
    today=date.today()
    Date = today.strftime("%B %d, %Y")
    now = datetime.now()
    current_time=now.strftime("%H:%M")
    Time=(current_time)
    #returns the Data and Time today
    return (Date,Time)

def Motivational_Quotes(filename):
    #reading file and splitting the data as the line changes
    lines=[]
    myfile=open(filename)
    txt=myfile.read()
    lst=txt.split("\n")
    #Randomly picks and 1 quote from the motivation.txt file and returns it
    for x in range(10):
         number=random.randint(0,100)
    return lst[number]

def format_for_printing_Timetable(Sorted_Table):
    #The purpose of this function is to arrange data so as to output in a table using tkinter
    #Division of Days done otherwise table becomes too wide
    lst=[]
    Days_of_week1=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY"]
    Days_of_week2=["FRIDAY","SATURDAY","SUNDAY",""]
    # used to ad space in the Table
    divider=["","","",""]

    lst.append(Days_of_week1)

    big_day1=max(len(Sorted_Table["MONDAY"]),len(Sorted_Table["TUESDAY"]),len(Sorted_Table["WEDNESDAY"]),len(Sorted_Table["THURSDAY"]))

    for a in range(big_day1):
        row=[]
        for i in Days_of_week1:

            if a>len(Sorted_Table[i])-1:
                row.append(" ")
            else:
                statement=(Sorted_Table[i][a][0]+" : "+Sorted_Table[i][a][1]+" -- "+Sorted_Table[i][a][2])
                row.append(statement)
        lst.append(row)


    big_day2=max(len(Sorted_Table["FRIDAY"]),len(Sorted_Table["SATURDAY"]),len(Sorted_Table["SUNDAY"]))
    lst.append(divider)
    lst.append(Days_of_week2)

    for a in range(big_day2):
        row=[]
        for i in Days_of_week2:
            if i not in Sorted_Table:
                row.append(" ")
            elif a>len(Sorted_Table[i])-1:
                row.append(" ")
            else:
                statement=(Sorted_Table[i][a][0]+" : "+Sorted_Table[i][a][1]+" -- "+Sorted_Table[i][a][2])
                row.append(statement)
        lst.append(row)
    print(lst)
    Table_output(lst)

def Table_output(lst):
    #code used to create and input data in a table inn tkinter
    class Table:

      def __init__(self,root):

       # code for creating table
       for i in range(total_rows):
           for j in range(total_columns):

               self.e = Entry(root, width=27, fg="Royalblue4",font=('Arial',12),bg="old lace")

               self.e.grid(row=i, column=j)
               self.e.insert(END, lst[i][j])

    total_rows = len(lst)
    total_columns = len(lst[0])

   # create root window
    root = Tk()
    t = Table(root)
    root.mainloop()

def partition(lst, start, end):
    pivot_p = (start+end)//2
    lst[pivot_p], lst[end] = lst[end], lst[pivot_p]
    pivot = lst[end]
    i = start
    for j in range(start, end):
        a=lst[j][1].split(":")
        b=pivot[1].split(":")

        if time(int(a[0]),int(a[1]))<= time(int(b[0]),int(b[1])):
            lst[i], lst[j] = lst[j], lst[i]
            i = i + 1
    lst[i], lst[end] = lst[end], lst[i]
    return i

def quickS(lst, start, end):
    if start < end:
        position = partition(lst, start, end)
        quickS(lst, start, position-1)
        quickS(lst, position+1, end)
    return lst

def quick_sort(lst):
    start = 0
    end = len(lst)-1
    return quickS(lst, start, end)

def Sorting_Schedule(Table,Day_Start,Day_end):
    a=1
    #goes to each day picks the events sorts them using quick sort
    #then puts it ack in the original dictionary(Sorted_Table)
    for day in Table:
        events=Table[day]
        sorted_events=quick_sort(events)
        Table[day]=sorted_events

    #this part is checking for clashes

    Clash="False"
    for Day in Table:
        #Linearly comparing times to see if there is a clash
        #A clash is detected if ending time of an event is greater than starting time of another event
        for a in range(len(Table[Day])-1):
            start_time=Table[Day][a][1]
            end_time=Table[Day][a][2]
            st_break=start_time.split(":")
            end_break=end_time.split(":")
            if a>=0:
                next_event_start=Table[Day][a+1][1]
                next_event_end=Table[Day][a+1][2]
                next_st_break=next_event_start.split(":")
                next_end_break=next_event_end.split(":")
                if time(int(end_break[0]),int(end_break[1]))>time(int(next_st_break[0]),int(next_st_break[1])):
                    Clash="True"
                    Statement=("There is a clash  between" + "  ===> "+ (" : ".join(Table[Day][a][:-1]))+ "  and   "+ (" : ".join(Table[Day][a+1][:-1]))+ "  on  "+ Day)
                    FreeTimeSlots,Time_periods=Free_Time_Slots(Table,Day_Start,Day_end)
                    Options=("You may choose some other time slot for your task from the following options")
                    print(Options)

                    for key,value in FreeTimeSlots.items():
                        print (key,value)


            #checking the first event of every day (flags it if lies before starting of Work Day)
            if a==0:
                if int(st_break[0])<int(Day_Start[:1]):
                    print(" : ".join(Table[Day][a][:-1])+ " Event is Starting before Work Day")
            #checking the last event of every day (flags it if lies after ending of Work Day)
            if a==(len(Table[Day])-2):
                if int(next_end_break[0])>=int(Day_end[:2]) and int(next_end_break[1])>int(Day_end[3:]):
                    print(" : ".join(Table[Day][a+1][:-1])+ " Event is ending after Work Day")
    #
    if Clash=="True":
        return {}
    else:
        return Table

def difference(h1, m1, h2, m2):
    #This functon helps to calculate the time-difference between 2 times xx:yy and xx:yy
    #The time difference is calculated in hours
    m1=int(m1)
    m2=int(m2)
    h1=int(h1)
    h2=int(h2)
    t1 = h1 + (m1/60)
    t2 = h2 + (m2/60)
    diff = round((t2-t1),4)
    return diff

def Time_journal_Days(Table):
    #This function linearly iterates over the Sorted_Table(dictioary)
    #finds the time spent on each task
    #adds it up and apends it in the list (Total_time)
    #with the index number of the list(Total_time) representing each day of the week
    Total_Time=[]
    for day in Table:
        Total=0
        for i in Table[day]:
            end_time=i[2].split(":")
            start_time=i[1].split(":")
            time=difference(start_time[0], start_time[1],end_time[0], end_time[1])
            Total+=time
        Total_Time.append(Total)
    return Total_Time

def Time_journal_Subjects(Sorted_Table):
    #this function first creates dictionary containing all items that are classified as work as keys
    Total_Time_Subjects={}
    for Day in Sorted_Table:
        for event in Sorted_Table[Day]:
            if event[3]=="Work":
                Total_Time_Subjects[event[0]]=0


    # this again iterates over the table, picks events that are classified as work
    #calculates their time difference and add it as a value to that event
    for day in Sorted_Table:
        Total=0
        events=Table[day]
        for i in events:
            if i[0] in Total_Time_Subjects:
                end_time=i[2].split(":")
                start_time=i[1].split(":")
                time=difference(start_time[0], start_time[1],end_time[0], end_time[1])
                prev=Total_Time_Subjects[i[0]]
                Total_Time_Subjects[i[0]]=prev+time

    Subjects=Total_Time_Subjects.keys()
    Time_per_Subject=Total_Time_Subjects.values()
    return (Subjects,Time_per_Subject)

def Productivity_Bar_Grpahs(Time_journal,objects):
    #takes values for the y-axis and objects as items on the x-axis
    y_pos = np.arange(len(objects))
    lst=['red', 'blue', 'purple', 'green', 'lavender', "yellow","orange","blue","fuchsia","purple",'purple', 'green', 'lavender', "yellow", 'blue', 'purple', 'green', 'lavender', "yellow","orange","blue","purple",'purple', 'green', 'lavender', "yellow"]
    plt.bar(y_pos, Time_journal, align='center', alpha=0.99,color=lst[:len(objects)+1])
    plt.xticks(y_pos, objects,rotation=10,fontweight='semibold', fontsize='10', horizontalalignment='center')
    plt.ylabel('Number of hours worked')
    plt.title('Productivity')
    plt.show()

def format_for_printing_Freetimeslots(FreeTimeSlots):
    #purpose of the function is to re-arrange dat from the dict to print in a table
    #Division of Days done otherwise table becomes too wide
    lst=[]
    Days_of_week1=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY"]
    Days_of_week2=["FRIDAY","SATURDAY","SUNDAY",""]
    divider=["","","",""]

    lst.append(Days_of_week1)
    #finds the max number of tasks at any given day--(to create that many rows in the table)
    big_day1=max(len(FreeTimeSlots["MONDAY"]),len(FreeTimeSlots["TUESDAY"]),len(FreeTimeSlots["WEDNESDAY"]),len(FreeTimeSlots["THURSDAY"]))

    #
    for a in range(big_day1):
        row=[]
        for i in Days_of_week1:
            if a>len(FreeTimeSlots[i])-1:
                row.append(" ")
            else:
                statement=(FreeTimeSlots[i][a])
                row.append(statement)
        lst.append(row)


    big_day2=max(len(FreeTimeSlots["FRIDAY"]),len(FreeTimeSlots["SATURDAY"]),len(FreeTimeSlots["SUNDAY"]))
    lst.append(divider)
    lst.append(Days_of_week2)

    for a in range(big_day2):
        row=[]
        for i in Days_of_week2:
            if i not in FreeTimeSlots:
                row.append(" ")
            elif a>len(FreeTimeSlots[i])-1:
                row.append(" ")
            else:
                statement=(FreeTimeSlots[i][a])
                row.append(statement)
        lst.append(row)
    print(lst)
    Table_output(lst)

def helper_free_time_slots(Sorted_Table,d_start,d_end):
    #Dict Free_Time_Slots collects free time slots for each day of the Days_of_week
    #Dic Time_Periods  saves the time period of each free slot for each day
    FreeTimeSlots={}
    Time_periods={}
    #setting up the dictionaries with days of the week as their keys
    for day in Sorted_Table:
        FreeTimeSlots[day]=[]
        Time_periods[day]=[]
        d_start="8:00"
        d_end="23:30"
        for event in Sorted_Table[day]:
            d_break=d_start.split(":")
            ev_start=event[1]
            ev_break=event[1].split(":")
            diff=difference(d_break[0],d_break[1], ev_break[0], ev_break[1])
            #only includes those timeslots that are above 30min
            if diff*60>30:
                FreeTimeSlots[day].append((d_start+"-"+ev_start))
                Time_periods[day].append(diff)
            d_start=event[2]
        d_break=d_end.split(":")
        ev_break=d_start.split(":")
        diff=difference(ev_break[0],ev_break[1], d_break[0], d_break[1])
        if diff*60>30:
            FreeTimeSlots[day].append((d_start+"-"+d_end))
            Time_periods[day].append(diff)

    return(FreeTimeSlots,Time_periods)

def Free_Time_Slots(Sorted_Table,d_start,d_end):
    FreeTimeSlots,Time_periods=helper_free_time_slots(Sorted_Table,d_start,d_end)
    return(FreeTimeSlots,Time_periods)

def Pie_Charts(Sorted_Table):
    Division=[]
    Total_Work=0
    Total_Leisure=0
    Total_Hobby=0
    for Day in Sorted_Table:
        for event in Sorted_Table[Day]:
            if event[3].upper()=="WORK":
                end_time=event[2].split(":")
                start_time=event[1].split(":")
                time=difference(start_time[0], start_time[1],end_time[0], end_time[1],)
                Total_Work+=time
            elif event[3].upper()=="HOBBY":
                end_time=event[2].split(":")
                start_time=event[1].split(":")
                time=difference(start_time[0], start_time[1],end_time[0], end_time[1])
                Total_Hobby+=time
            elif event[3].upper()=="LEISURE":
                end_time=event[2].split(":")
                start_time=event[1].split(":")
                time=difference(start_time[0], start_time[1],end_time[0], end_time[1],)
                Total_Leisure+=time

    Division.append(Total_Work)
    Division.append(Total_Hobby)
    Division.append(Total_Leisure)
    activities = ['Work', 'Hobbies', 'Leisure']

    # color for each label
    colors = ['r', 'y', 'g']
    # plotting the pie chart
    plt.pie(Division, labels = activities, colors=colors,
            startangle=90, shadow = True, explode = (0, 0, 0.1),
            radius = 1.2, autopct = '%1.1f%%')

    # plotting legend
    plt.legend(title="Time Division")

    # showing the plot
    plt.show()

def format_for_printing_Todo_list(Todolist):
    lst=[]
    Days_of_week1=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY"]
    Days_of_week2=["FRIDAY","SATURDAY","SUNDAY",""]
    divider=["","","",""]

    lst.append(Days_of_week1)
    print(len(Todolist["WEDNESDAY"]))

    big_day1=max(len(Todolist["MONDAY"]),len(Todolist["TUESDAY"]),len(Todolist["WEDNESDAY"]),len(Todolist["THURSDAY"]))

    for a in range(big_day1):
        row=[]
        for i in Days_of_week1:

            if a>len(Todolist[i])-1:
                row.append(" ")
            else:
                statement=(Todolist[i][a][0]+" at "+Todolist[i][a][1])
                row.append(statement)
        lst.append(row)


    big_day2=max(len(Todolist["FRIDAY"]),len(Todolist["SATURDAY"]),len(Todolist["SUNDAY"]))
    lst.append(divider)
    lst.append(Days_of_week2)

    if big_day2==0:
        lst.append(divider)
    else:

        for a in range(big_day2):
            row=[]
            for i in Days_of_week2:
                if i not in Todolist:
                    row.append(" ")
                elif a>len(Todolist[i])-1:
                    row.append(" ")
                else:
                    statement=(Todolist[i][a][0]+" at "+Todolist[i][a][1])
                    row.append(statement)
            lst.append(row)
    print(lst)
    Table_output(lst)

def To_do_List(Reminders):
    Reminders.pop(0)                                                              #removing the heading(reminder. Day, Time)
    Todolist ={}
    Days_of_the_week=["MONDAY","TUESDAY","WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]        #setting up the basic dictionary with days of the week
    for day in Days_of_the_week:
        Todolist[day]=[]

    for i in range(len(Reminders)):
        for j in range(len(Reminders[i])):
            if j==1:                                                               #stopping at the second column where user has entered the days
                Repeat=convert_days_to_fullform(Reminders[i][j])                   #calling function to convert (MT)-->[MONDAY,TUESDAY]
                for day in Repeat:                                                 #Repeat is a list containing full form of days entered by user(repition days)
                    day=day.upper()
                                                                                        #coverting to uppercase
                    Todolist[day].append([Reminders[i][0],Reminders[i][2]])          #appending event,start time


    for day in Todolist:
        events=Todolist[day]
        events.sort(key = lambda x: x[1])
        Todolist[day]

    return Todolist

def new_time_insert(start_time,diff):
    diff=round(diff,3)
    t1=dt.datetime.strptime(start_time,"%H:%M")
    x = t1 + timedelta(hours=diff)
    new_end_time=str((x.time()))
    return (new_end_time[:5])

def Rewrite_Excel_File(Data,Heading,Reminders):
    Data.insert(0,Heading)
    Data.append(["","","","",""])
    Data.append(["","","","",""])
    Data.append(["Reminder","Repeat","Time"])
    for i in Reminders:
        Data.append(i)
    with open("Schedule.csv", mode="w",newline="") as csvfile:
        fav=csv.writer(csvfile)
        fav.writerows(Data)

def Automatic_rescheduler(Sorted_Table,Day,FreeTimeSlots,Time_periods,Data,Heading,Reminders,d_start,d_end,box):
    Options={}
    Task_Numbers=tasknumber.get()
    Day=Day.upper()
    if int(Task_Numbers)>len(Sorted_Table[Day]) or int(Task_Numbers)<=0:
        box.insert("end","Task Number is not valid")
        return


    count=1
    Incomplete_work=[]
    Days_of_the_week=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    Symbols=["M","T","W","R","F","S","U"]
    day_number=Days_of_the_week.index(Day)
    for x in Days_of_the_week:
        Options[x]=[]

    print(Task_Numbers)
    work=(Sorted_Table[Day][int(Task_Numbers)-1])

    print(work)
    print(Sorted_Table)
    print("Free Time Slots",FreeTimeSlots)
    # print(Time_periods)
    count=1
    # for work in Incomplete_work:
    end_time=work[2].split(":")
    start_time=work[1].split(":")
    diff=difference(start_time[0], start_time[1],end_time[0], end_time[1])

    for a in range(day_number+1,7):
        Day=Days_of_the_week[a]
        for i in range(len(Time_periods[Day])):
            if Time_periods[Day][i]>= diff:
                Options[Day].append((count,FreeTimeSlots[Day][i]))
                count+=1



        #Printing Options
    for key,value in Options.items():
            if len(value) >0:
                statement=key+str(value)
                box.insert("end",statement)

def part2(Sorted_Table,Day,FreeTimeSlots,Time_periods,Data,Heading,Reminders,d_start,d_end,box):
    Day=Day.upper()
    num=int(optionnumber.get())
    Options={}
    Task_Numbers=int(tasknumber.get())
    if int(Task_Numbers)>len(Sorted_Table[Day]) or int(Task_Numbers)<=0:
        box.insert("end","Task Number is not valid")
        return

    count=1
    Incomplete_work=[]
    Days_of_the_week=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    Symbols=["M","T","W","R","F","S","U"]
    day_number=Days_of_the_week.index(Day)
    for x in Days_of_the_week:
        Options[x]=[]

    print(Task_Numbers)
    work=(Sorted_Table[Day][int(Task_Numbers)-1])

    print(work)
    print(Sorted_Table)
    print("Free Time Slots",FreeTimeSlots)
    # print(Time_periods)
    count=0
    # for work in Incomplete_work:
    end_time=work[2].split(":")
    start_time=work[1].split(":")
    diff=difference(start_time[0], start_time[1],end_time[0], end_time[1])

    for a in range(day_number+1,7):
        Day=Days_of_the_week[a]
        for i in range(len(Time_periods[Day])):
            if Time_periods[Day][i]>= diff:
                Options[Day].append((count+1,FreeTimeSlots[Day][i]))
                count+=1

    if count==0:
        box.insert("end","You have a very busy Schedule :)")
        return

    if int(num)>count or int(num)<=0:
        box.insert("end","Option Number is not valid")
        return


    for key, value in Options.items():
        for i in value:
            if i[0]==num:
                Sorted_Table[key].append([work[0],i[1][:4],i[1][5:],work[3]])
                #sorting events for that day only
                events=Table[key]
                sorted_events=quick_sort(events)
                Sorted_Table[key]=sorted_events
                #recalibrating FreeTimeSlots
                FreeTimeSlots,Time_periods=Free_Time_Slots(Sorted_Table,d_start,d_end)
                for a in range(len(Data)):
                    if Data[a][0]==work[0] and work[1]==Data[a][2]:
                        #alter current entry
                        current_days_repeat=Data[a][1]
                        if len(current_days_repeat)>1:
                            new_days_repeat=current_days_repeat.replace(Symbols[day_number],"")
                            Data[a][1]=new_days_repeat
                        else:
                            Data.pop(a)
                        #add a new entry
                        time_slot=i[1].split(":")

                        if int(time_slot[0])<9:
                            n_end_time=new_time_insert(i[1][:4],diff)
                        else:
                            n_end_time=new_time_insert(i[1][:5],diff)

                        Data.append([work[0],Symbols[Days_of_the_week.index(key)],i[1][:5],n_end_time,work[3]])

                        print(Data)
                        Rewrite_Excel_File(Data,Heading,Reminders)
                        statement="Your task has successfully been"
                        box.insert("end",statement)
                        box.insert("end","Rescheduled.")

                        print(Sorted_Table)
                        break




# Personalized USER Details
Name="mohid"
Name=Name.upper()
Day_Start="8:00"
Day_end="23:30"



filename="Schedule.csv"
Data,Heading,Reminders=(readcsv(filename))
Table=Organize(Data)
Date,Time=(Date_Today(today=0))
filename="motivational.txt"
Moti_Quote=Motivational_Quotes(filename)
Sorted_Table=(Sorting_Schedule(Table,Day_Start,Day_end))
Total_Time=(Time_journal_Days(Sorted_Table))
Objects = ['MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
Subjects,Time_per_Subject=Time_journal_Subjects(Sorted_Table)
FreeTimeSlots,Time_periods=Free_Time_Slots(Sorted_Table,Day_Start,Day_end)
Todolist=To_do_List(Reminders)
Day=datetime.today().strftime('%A').upper()


# Creating tkinter window with fixed geometry
root = Tk()
root.geometry('670x560')
root.title("Scheduling Assistant")

#Inserting BAckground
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

image = Image.open('new_image.png')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)

# Inserting the motivational quote with formatting"
if len(Moti_Quote)>170:
    first_half=Moti_Quote[:85]
    sec_half=Moti_Quote[85:170]
    third_half=Moti_Quote[170:]
    label_frame = tk.Label(root, text=first_half,font=("Arial semibold",8)).place(x=70,y=250)
    label_frame = tk.Label(root, text=sec_half,font=("Arial semibold",8)).place(x=70,y=270)
    label_frame = tk.Label(root, text=third_half,font=("Arial semibold",8)).place(x=70,y=290)
elif len(Moti_Quote)>85:
    first_half=Moti_Quote[:85]
    sec_half=Moti_Quote[85:]
    label_frame = tk.Label(root, text=first_half,font=("Arial semibold",8)).place(x=70,y=250)
    label_frame = tk.Label(root, text=sec_half,font=("Arial semibold",8)).place(x=70,y=270)
else:
    label_frame = tk.Label(root, text=Moti_Quote,font=("Arial semibold",8)).place(x=70,y=250)

 # This will create a LabelFrame for time and Date and Day
label_frame = tk.Label(root, text=Time,font=("Arial",35),fg="brown4").place(x=265,y=10)
label_frame = tk.Label(root, text=Date,font=("Arial",12),fg="brown4").place(x=275,y=65)
label_frame = tk.Label(root, text=Day,font=("Arial",10),fg="brown4").place(x=282,y=85)

#Initializing Greeting depending on the time of the day
if int(Time[:2])<12:
   gret="GOOD MORNING, "+Name+"."
   greeting = tk.Label(text=gret,font=("Arial Bold",18),fg="brown")
   greeting.place(x=190,y=120)
elif int(Time[:2])>11 and int(Time[:2])<17:
    gret="GOOD AFTERNOON, "+Name+"."
    greeting = tk.Label(text=gret,font=("Arial Bold",18),fg="brown")
    greeting.place(x=190,y=120)
else:
   gret="GOOD EVENING, "+Name+"."
   greeting = tk.Label(text=gret,font=("Arial Bold",18),fg="brown")
   greeting.place(x=190,y=120)

#Buttons
photo = PhotoImage(file = r"timetable.png")
timetable_img = photo.subsample(9, 9)

btn1=tk.Button (root, text="Timetable",font=('Arial semibold', 12),image=timetable_img, compound=LEFT,fg="green",relief=RAISED,command=lambda:(format_for_printing_Timetable(Sorted_Table)))
btn1.place(x=85,y=218)

photo = PhotoImage(file = r"freetimeslots.png")
free_img = photo.subsample(9, 9)

btn1=tk.Button (root, text="Free-Time-Slots",font=('Arial semibold', 12), image=free_img, compound=LEFT,fg="green",relief=RAISED,command=lambda:  format_for_printing_Freetimeslots(FreeTimeSlots))
btn1.place(x=225,y=218)

photo = PhotoImage(file = r"reminders.png")
reminders_img = photo.subsample(9, 10)

btn1=tk.Button (root, text="Reminders", font=('Arial semibold', 12),fg="green", image=reminders_img, compound=LEFT,relief=RAISED,command=lambda:format_for_printing_Todo_list(Todolist))
btn1.place(x=405,y=218)

#Drop down Menu for Graphs:
def show():
    label.config( text = clicked.get() )

# Dropdown menu options
options = ["Daily Productivity","Time-Journal","Pie-chart"]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set( "Choose a Productivity Graph" )

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.place(x=165, y=310)
# Set the background color of Options Menu to green
drop.config(fg="darkgreen",font=("Arial",10,"bold"))
drop["menu"].config(bg="peach puff",fg="blue4",font=("Arial",10))


#linking to Productivity Graphs
def change_dropdown(*args):
    a=options.index(clicked.get())
    if a == 0:
        Productivity_Bar_Grpahs(Total_Time,Objects)
    elif a==1:
        Productivity_Bar_Grpahs(Time_per_Subject,Subjects)
    else:
        Pie_Charts(Sorted_Table)

# link function to change dropdown
clicked.trace('w', change_dropdown)

#Interface for Rescheduling
label_frame = tk.Label(root, text="Task No.",font=("Arial",10),fg="brown4").place(x=62,y=355)

tasknumber=Entry(root)
tasknumber.place(x=70,y=380,height = 15,width = 45)

#helps to clear the output box
def delete():
   box.delete(0,"end")

label_frame = tk.Label(root, text="Option No.",font=("Arial",10),fg="brown4").place(x=58,y=430)
optionnumber=Entry(root)
optionnumber.place(x=72,y=455,height = 15,width = 42)

b1= Button(root, text= "Clear",command= delete)
b1.place(x=72,y=400)

btn1=tk.Button (root, text="Show Options", font=('Arial semibold', 8),fg="brown4",relief=RAISED,command=lambda:Automatic_rescheduler(Sorted_Table,Day,FreeTimeSlots,Time_periods,Data,Heading,Reminders,Day_Start,Day_end,box))
btn1.place(x=205,y=345)

box=Listbox(root,width=51,height=7)
box.place(x=123,y=380)

btn1=tk.Button (root, text="Submit", font=('Arial semibold', 8),fg="brown4",relief=RAISED,command=lambda:part2(Sorted_Table,Day,FreeTimeSlots,Time_periods,Data,Heading,Reminders,Day_Start,Day_end,box))
btn1.place(x=285,y=345)


 # This creates infinite loop which generally
 # waits for any interrupt (like keyboard or
 # mouse) to terminate
root.mainloop()
