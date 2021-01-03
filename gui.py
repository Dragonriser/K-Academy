########################################K ACADEMY############################################
#~Imports~
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk ,Image
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import bcrypt
import os.path 
import mysql.connector
import random
import time
from github import Github
import pickle
import urllib
import pikepdf
from pdf2docx import Converter
import shutil
import os
import docx2txt
import datetime
from pathlib import Path
from random import randint
import shutil
#~Database~#
mydb = mysql.connector.connect(
    host="sql2.freesqldatabase.com",
    user="sql2384560",
    password="aZ2*rY8*",
    database="sql2384560"
)

mycursor = mydb.cursor()

def printDatabase():
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def deleteUser(userUsername):
    sql = "DELETE FROM users WHERE username = %s"
    usrnm = (userUsername, )
    mycursor.execute(sql, usrnm)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")

def passwordUpdate(oldPass, newPass):
    mycursor = mydb.cursor()
    sql = "UPDATE users SET password = %s WHERE password = %s"
    oldnew = (oldPass, newPass,)
    mycursor.execute(sql, oldnew)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def addColumnToTable(columnname):
    sql = "ALTER TABLE users ADD %s INT(15)" % (columnname)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.execute("SHOW columns FROM users")
    print('Current row headings: ', [column[0] for column in mycursor.fetchall()])

def deleteColumnFromTable(columnname):
    sql = "ALTER TABLE users DROP %s" % (columnname)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.execute("SHOW columns FROM users")
    print('Current row headings: ', [column[0] for column in mycursor.fetchall()])

#mydb.close()

#~Globals~#
UI = None
loginFrame = None
createAccountFrame = None
dashboardFrame = None
settingsFrame = None
homeScreenFrame = None
resourcesSCF = None
usernameEntry = None
passWord = None
logo = None
userData = None
useroverviewFrame = None
sidedash = None

dashboardButton = None
ResourcesButton = None
settingsButton = None

#~Constants~#

#~General
LOGOFILE = os.path.dirname(__file__) + "\\logo.png"
DASHBOARDFILE = os.path.dirname(__file__) + "\\dashboard.png"
HUMANFILE = os.path.dirname(__file__) + "\\humangraphic.png"
SALT = bcrypt.gensalt()

#~Flags
NEW_USER = False
PAGE = ''
USERNAME = ''
HS = 0

#~Colours
GREY = '#363636'
IVORY = '#FBFBFB'
IVORY2 = '#F9F9F4'
BLACK = '#2E2F30'
BLUE = '#8CAEAF'
WHITE = '#FFFFFF'


#~Courses
SUBJECTS = []
LEVELS = []
BOARDS = []
allCourses = {}
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
PAGESTARTDELIM = "|||~~~###///PGSTDELIM///###~~~|||"
PAGEENDDELIM = "|||~~~###///PGEDDELIM///###~~~|||"

resourceMap = []
monthNumberMap = {"jan" : 1, "feb" : 2, "mar" : 3, "apr" : 4, "may" : 5, "jun" : 6, "jul" : 7, "aug" : 8, "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}
ROMANNUMERALDIGITS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]

#~Scrollable frame (classes magic)~
class ScrollableFrame(tk.Frame):
    def __init__(self, container, verticalSB = True, horizontalSB = False, height= -1, width=-1, *args, **kwargs):
        """Pass in height, width and background colour"""
        super().__init__(container, *args, **kwargs)
        if verticalSB and horizontalSB:
            raise ValueError("Cannot have more than one scrollbar in a window.\n Please put horizontal Scrollable frame IN vertical one")

        if height == -1 and width == -1:
            self.canvas = tk.Canvas(self,highlightthickness=0)
        else:
            self.canvas = tk.Canvas(self, height = height, width = width, highlightthickness=0)

        if verticalSB:
            vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        if horizontalSB:
            hscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollableFrame = tk.Frame(self.canvas)
        self.scrollableFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        if verticalSB:
            self.canvas.configure(yscrollcommand=vscrollbar.set)
        if horizontalSB:
            self.canvas.configure(xscrollcommand=hscrollbar.set)
        
        if verticalSB:
            vscrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True, anchor = 'nw')
        if horizontalSB:
            hscrollbar.pack(side="bottom", fill="x")
            self.canvas.pack(side="top", fill="both", expand=True, anchor = 'nw')

        self.canvas.bind('<Configure>', self.FrameWidth)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

#~UI~#
def start():
    #initialising the main window
    startUI = tk.Tk()
    startUI.state('zoomed')
    #startUI.configure(bg='#D1D4E7')
    startUI.title('K Academy')
    icon = ImageTk.PhotoImage(Image.open(LOGOFILE))
    icon.image = LOGOFILE
    startUI.iconphoto(False, icon)
    startUI.minsize(900, 600)

    startUI.bind('<Return>', lambda e, f = startUI : storage(f))
    return startUI


def login(parentWindow):
    global loginFrame
    global usernameEntry
    global passWord
    global logo
    NEW_USER = False
    PAGE = 'login'
    destroyWindows()

    loginFrame = tk.Frame(
        parentWindow,
        bg = GREY,
        bd = 0
    )

    loginFrame.pack(
        expand = True,
        fill = tk.BOTH
    )
    
    loginFrame.grid_columnconfigure(0, weight = 1)
    loginFrame.grid_columnconfigure(1, minsize=100)
    loginFrame.grid_columnconfigure(2, minsize=100)
    loginFrame.grid_columnconfigure(3, weight = 1)

    logo = (Image.open(LOGOFILE))
    logo = logo.resize((400, 400), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo)

    logoLabel = tk.Label(
        loginFrame,
        bg = '#EDE9F2',
        bd = 0,
        image = logo
    )

    logoLabel.grid(column = 1, columnspan = 2, row = 0, padx = (30, 30), pady = (0, 10))

    usernameEntry = tk.Entry(
        loginFrame,
        bg = '#ffffff',
        bd = 1, 
        font = ('verdana', 12), 
        fg = '#f0000f', 
        )

    usernameEntry.delete(0, 'end')
    usernameEntry.insert(0, 'username')
    usernameEntry.bind('<FocusIn>', lambda e,f = usernameEntry:on_entry_click(e,f))
    usernameEntry.bind('<FocusOut>', lambda e,f = usernameEntry:on_focusout(e,f))
    usernameEntry.config(fg = 'grey')
    usernameEntry.grid(column = 1, columnspan = 2, row = 1, padx = (30, 30), pady = (0, 0))

    passWord = tk.Entry(
        loginFrame,
        text ='forms', 
        bg = '#ffffff', 
        bd = 1, 
        font = ('verdana', 12), 
        fg = '#f0000f', 
        #show = '•', 
        )

    passWord.delete(0, 'end')
    passWord.insert(0, 'password')
    passWord.bind('<FocusIn>', lambda e,f = passWord:on_entry_clickHidden(e,f))
    passWord.bind('<FocusOut>', lambda e,f = passWord:on_focusoutHidden(e,f))
    passWord.config(fg = 'grey')
    passWord.grid(column = 1, columnspan = 2, row = 2, padx = (30, 30), pady = (10, 10))
    loginButton = tk.Button(
        loginFrame,
        text = 'login',
        bg = BLUE,
        activebackground = '#BFD4E7',
        bd = 0,
        command = lambda e = parentWindow: storage(e)
    )
    loginButton.grid(column = 2, row = 3, sticky = 'W', padx = (50, 50), pady = (10, 10))

    newAccountButton = tk.Button(
        loginFrame,
        text = 'new user?',
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e = parentWindow: createAccount(e)
    )
    newAccountButton.grid(column = 1, row = 3, sticky = 'E', padx = (50, 50), pady = (10, 10))


def on_entry_click(event, box):
    if box.cget('fg') == 'grey':
        box.delete(0, "end") # delete all the text in the usernameEntry1
        box.insert(0, '') #Insert blank for user input
        box.config(fg = 'black')

def on_focusout(event, box):
    if box.get() == '':
        box.insert(0, 'username')
        box.config(fg = 'grey')

def on_entry_clickHidden(event, box):
    if box.cget('fg') == 'grey':
        box.delete(0, "end") 
        box.insert(0, '') 
        box.config(fg = 'black', show = '•')
        
def on_focusoutHidden(event, box):
    if box.get() == '':
        box.insert(0, 'password')
        box.config(fg = 'grey', show = '')


def createAccount(parentWindow):
    global NEW_USER
    global PAGE
    global createAccountFrame
    global usernameEntry
    global passWord
    global logo
    NEW_USER = True
    PAGE = 'create account'

    destroyWindows()

    createAccountFrame = tk.Frame(
        parentWindow,
        bg = GREY,
        bd = 0
    )

    createAccountFrame.pack(
        expand = True,
        fill = tk.BOTH)
    
    createAccountFrame.grid_columnconfigure(0, weight = 1)
    createAccountFrame.grid_columnconfigure(1, minsize=100)
    createAccountFrame.grid_columnconfigure(2, minsize=100)
    createAccountFrame.grid_columnconfigure(3, weight = 1)

    logo = (Image.open(LOGOFILE))
    logo = logo.resize((400, 400), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo)

    logoLabel = tk.Label(
        createAccountFrame,
        bg = '#EDE9F2',
        bd = 0,
        image = logo
    )

    logoLabel.grid(column = 1, columnspan = 2, row = 0, padx = (30, 30), pady = (0, 10))


    usernameEntry = tk.Entry(
        createAccountFrame,
        bg = '#ffffff',
        bd = 1, 
        font = ('verdana', 12), 
        fg = '#f0000f', 
        )

    usernameEntry.delete(0, 'end')
    usernameEntry.insert(0, 'username')
    usernameEntry.bind('<FocusIn>', lambda e,f = usernameEntry:on_entry_click(e,f))
    usernameEntry.bind('<FocusOut>', lambda e,f = usernameEntry:on_focusout(e,f))
    usernameEntry.config(fg = 'grey')
    usernameEntry.grid(column = 1, columnspan = 2, row = 1, padx = (30, 30), pady = (0, 0))

    passWord = tk.Entry(
        createAccountFrame,
        text ='forms', 
        bg = '#ffffff', 
        bd = 1, 
        font = ('verdana', 12), 
        fg = '#f0000f', 
        #show = '•', 
        )

    passWord.delete(0, 'end')
    passWord.insert(0, 'password')
    passWord.bind('<FocusIn>', lambda e,f = passWord:on_entry_clickHidden(e,f))
    passWord.bind('<FocusOut>', lambda e,f = passWord:on_focusoutHidden(e,f))
    passWord.config(fg = 'grey')
    passWord.grid(column = 1, columnspan = 2, row = 2, padx = (30, 30), pady = (10, 10))

    createButton = tk.Button(
        createAccountFrame,
        text = 'create',
        bg = BLUE,
        activebackground = '#BFD4E7',
        bd = 0,
        command = lambda e=parentWindow: storage(e)
    )

    createButton.grid(column = 2, row = 3, sticky = 'W', padx = (50, 50), pady = (0, 0))
    backButton = tk.Button(
        createAccountFrame,
        text = '↩',
        font = ('verdana', 18),
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e=parentWindow : login(e)
    )

    backButton.grid(column = 1, row = 3, sticky = 'E', padx = (50, 50), pady = (0, 0))

def storage(parentWindow):
    global USERNAME
    global userData
    if NEW_USER == True:
        newUsername = usernameEntry.get()
        newPassword = passWord.get()
        sql = 'SELECT * FROM `users` WHERE `username` = %s'
        val= (newUsername,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        rowCount = mycursor.rowcount
        if rowCount > 0:
            inUseUI = tk.Tk()
            inUseUI.title('K Academy')
            #icon = ImageTk.PhotoImage(Image.open("C:\\Users\\jacqu\\Documents\\Home\\Coding\\Python\\.vscode\\Programs\\PS\\UniversityComparison\\LOGOFILE.png"))
            #icon.image = "C:\\Users\\jacqu\\Documents\\Home\\Coding\\Python\\.vscode\\Programs\\PS\\UniversityComparison\\LOGOFILE.png"
            #inUseUI.iconphoto(False, icon)
            inUseUI.minsize(100, 100)

            inUseLabel = tk.Label(inUseUI, text = 'Username already exists')
            inUseLabel.grid(padx = (10, 10), pady = (10, 10))

            inUseUI.mainloop()
        else:
            newPassword = bcrypt.hashpw(newPassword.encode('utf8'), SALT)
            sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
            val = (newUsername, newPassword)
            mycursor.execute(sql, val)
            mydb.commit()
            USERNAME = newUsername
            getUserData(USERNAME)
            userData.schedule()
            homeScreen(parentWindow)
    else:
        oldusername = usernameEntry.get()
        oldpassword = passWord.get()
        sql = 'SELECT * FROM `users` WHERE `username` = %s'
        val = (oldusername,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        rowCount = mycursor.rowcount
        if rowCount == 0:
            wrongUsnPwd('username')
        else:
            dbhashedpwd = myresult[0][1]
            if bcrypt.checkpw(oldpassword.encode('utf8'), dbhashedpwd.encode('utf8')):
                USERNAME = oldusername
                getUserData(USERNAME)
                userData.schedule()
                homeScreen(parentWindow)
            else:
                wrongUsnPwd('password')

def wrongUsnPwd(userorpwd):
    wrongDetailsUI = tk.Tk()
    wrongDetailsUI.title('K Academy')
    #icon = ImageTk.PhotoImage(Image.open("C:\\Users\\jacqu\\Documents\\Home\\Coding\\Python\\.vscode\\Programs\\PS\\UniversityComparison\\LOGOFILE.png"))
    #icon.image = "C:\\Users\\jacqu\\Documents\\Home\\Coding\\Python\\.vscode\\Programs\\PS\\UniversityComparison\\LOGOFILE.png"
    #wrongDetailsUI.iconphoto(False, icon)
    wrongDetailsUI.minsize(100, 100)

    wrongDetailsLabel = tk.Label(wrongDetailsUI, text = 'incorrect ' + userorpwd)
    wrongDetailsLabel.grid(padx = (10, 10), pady = (10, 10))

    wrongDetailsUI.mainloop()


def homeScreen(parentWindow):
    global PAGE
    global dashboardButton 
    global ResourcesButton 
    global settingsButton
    global USERNAME
    global HS
    global DASHBOARDFILE
    global dashboardFrame
    global homeScreenFrame
    global useroverviewFrame
    global sidedash
    tryDestruction(useroverviewFrame)
    tryDestruction(sidedash)
    PAGE = 'home screen'

    destroyWindows()

    homeScreenFrame = tk.Frame(
            parentWindow,
            bg = '#eeeeee',
            bd = 0
        )

    homeScreenFrame.pack(
        expand = True,
        fill = tk.BOTH
    )

    homeScreenFrame.grid_columnconfigure(0, weight = 1)
    homeScreenFrame.grid_columnconfigure(1, minsize=50)
    homeScreenFrame.grid_columnconfigure(2, minsize=50)
    homeScreenFrame.grid_columnconfigure(3, minsize=50)
    homeScreenFrame.grid_columnconfigure(4, minsize=50)
    homeScreenFrame.grid_columnconfigure(5, weight = 1)
    homeScreenFrame.grid_rowconfigure(0, weight = 1)

    columnsTotal = homeScreenFrame.grid_size()[0]
    rowsTotal = homeScreenFrame.grid_size()[1]

    if rowsTotal == 0:
        rowsTotal = 2

    '''if NEW_USER:
        useronboarding = tk.Frame(
            homeScreenFrame,
            bg = GREY,
            bd = 1
        )

        useronboarding.grid(
            columnspan = columnsTotal,
            row = 0,
            padx = (100, 100),
            pady = (100, 100),
            sticky = tk.NSEW
            )
        
        useronboarding.destroy()'''
    
    #if HS == 0:

    sidedash = tk.Frame(
        homeScreenFrame,
        bg = WHITE,
        bd = 0,
        width = 300
    )

    sidedash.pack(
        expand = 0, 
        fill = tk.BOTH, 
        side = 'left', 
        anchor = 'nw'
    )

    dashboardButton = tk.Button(
        sidedash,
        text = '📰   Dashboard',
        justify = tk.LEFT,
        font = ('verdana, 12'),
        bd = 0,
        bg = WHITE,
        command = lambda e=homeScreenFrame: homeScreen(e)
    )

    dashboardButton.grid(
        column = 1,
        row = 0,
        sticky = tk.NW,
        padx = (10, 10),
        pady = (20, 20)
    )

    ResourcesButton = tk.Button(
        sidedash,
        text = '🗀   Resources',
        justify = tk.LEFT,
        font = ('verdana, 12'),
        bd = 0,
        bg = WHITE,
        command = lambda e=homeScreenFrame: resources(e)
    )

    ResourcesButton.grid(
        column = 1,
        row = 1,
        sticky = tk.NW,
        padx = (10, 10),
        pady = (20, 20)
    )

    settingsButton = tk.Button(
        sidedash,
        text = '⛭   Settings',
        justify = tk.LEFT,
        font = ('verdana, 12'),
        bd = 0,
        bg = WHITE,
        command = lambda e=homeScreenFrame: settings(e)
    )

    settingsButton.grid(
        column = 1,
        row = 2,
        sticky = tk.NW,
        padx = (10, 10),
        pady = (20, 20)
    )

    useroverviewFrame = tk.Frame(
        homeScreenFrame,
        bd = 0,
        bg = WHITE,
        width = 300
    )

    useroverviewFrame.pack(
        expand = 0, 
        fill = tk.BOTH, 
        side = 'right', 
        anchor = 'ne'
        )

    usericonLabel = tk.Label(
        useroverviewFrame,
        text = '🍵',
        font = ('verdana', '50'),
        fg = BLUE,
        bg = WHITE
    )

    usericonLabel.grid(
        column = 5,
        rowspan = 3,
        row = 0,
        padx = (75, 75),
        pady = (50, 20)
    )

    usernameLabelUseroverview = tk.Label(
        useroverviewFrame,
        text = USERNAME,
        font = ('verdana', '10', 'bold'),
        fg = GREY,
        bg = WHITE
    )

    usernameLabelUseroverview.grid(
        column = 5,
        row = 4,
        padx = (75, 75),
        pady = (0, 30),
        sticky = tk.NSEW
    )

    remindersLabel = tk.Label(
        useroverviewFrame,
        text = 'Reminders',
        font = ('verdana', '10', 'bold'),
        fg = '#000000',
        bg = WHITE,
        justify = tk.LEFT
    )    

    remindersLabel.grid(
        column = 5,
        row = 5,
        padx = (5, 145),
        pady = (50, 50),
        sticky = tk.W
    )

    for course in userData.studies:
        toDo = userData.getQuestionsToDo(course)
        print(toDo)

    dashboardFrame = tk.Frame(
        homeScreenFrame,
        bd = 0,
        bg = '#000000'
    )

    dashboardFrame.pack(
        expand = 1, 
        fill = tk.BOTH, 
        side = 'top', 
        anchor = 'n'
    )

    dashboardFrame.update()
    dframeheight = dashboardFrame.winfo_height()
    dframewidth = dashboardFrame.winfo_width()

    dashboardBackground = (Image.open(DASHBOARDFILE))
    dashboardBackground = dashboardBackground.resize((dframewidth, dframeheight), Image.ANTIALIAS)
    dashboardBackground = ImageTk.PhotoImage(dashboardBackground)

    dashboardImageLabel = tk.Label(
        dashboardFrame,
        bd = 0,
        image = dashboardBackground,
    )

    '''dashboardImageLabel.create_image(
        0,
        0,
        image = dashboardBackground
    )'''

    columnsTotal = homeScreenFrame.grid_size()[0]
    rowsTotal = homeScreenFrame.grid_size()[1]

    dashboardImageLabel.grid(
        column = 1, 
        columnspan = columnsTotal-1, 
        row = 0, 
        rowspan = rowsTotal, 
        padx = (0, 0), 
        pady = (0, 0)
    )

    dashboardImageLabel.image = dashboardBackground

    dashboardImageLabel.grid_propagate(0)

    #3/01/2021 <- Jacqueline
    #reminders - todays not done yet tests (the tests w/ no results submitted yet) '{subject} - {topic}' (put in max, eg 5)
    
    userLabel = tk.Label(
        dashboardImageLabel,
        text = 'Welcome ' + USERNAME + '!',
        font = ('verdana', 15, 'bold'),
        bg = BLUE,
        fg = IVORY,
        justify = tk.LEFT
    )

    userLabel.grid(
        column = 1,
        row = 1,
        padx = (100, 50),
        pady = (80, 20),
        sticky = tk.W
    )

    PERCENT = '50 %'

    percentLabel = tk.Label(
        dashboardImageLabel,
        text = 'You\'ve completed ' + PERCENT + ' of your goal this week.\n Keep it up and keep improving your results!',
        font = ('verdana', 11),
        bg = BLUE,
        fg = BLACK,
        justify = tk.LEFT
    )

    percentLabel.grid(
        column = 1,
        row = 2,
        padx = (100, 50),
        pady = (20, 50)
    )

    humanicon = (Image.open(HUMANFILE))
    humanicon = humanicon.resize((110, 150), Image.ANTIALIAS)
    humanicon = ImageTk.PhotoImage(humanicon)

    humaniconLabel = tk.Label(
        dashboardImageLabel,
        bd = 0,
        image = humanicon,
    )

    humaniconLabel.grid(
        column = 2,
        row = 1,
        rowspan = 2,
        padx = (90, 50),
        pady = (60, 50)
    )

    humaniconLabel.image = humanicon

    latestResultsLabel = tk.Label(
        dashboardImageLabel,
        text = 'Latest Results',
        font = ('verdana', 11, 'bold'),
        bg = IVORY,
        fg = BLACK,
        justify = tk.LEFT
    )

    latestResultsLabel.grid(
        column = 1,
        row = 3,
        padx = (90, 0),
        pady = (10, 10),
        sticky = tk.NW
    )

    subjectForScore = ['Bio', 'Chem', 'Maths', 'Physics', 'CS', 'Further']
    topicForScore = ['Topic 1', 'Topic 3', 'Topic 6', 'Topic 2', 'Topic 4', 'Topic 1']
    forScore = ['10/12', '3/4', '5/5', '13/15', '3/3']


    for i in range(5):
        homeScreenFrame.grid_rowconfigure(4+i, minsize = 50)
        label = {}
        label["Subject"] = tk.Label(dashboardImageLabel, text = subjectForScore[i], font = ('verdana', 8, 'bold'), fg = BLACK, bg = IVORY, justify = tk.LEFT) 
        label["Subject"].grid(column = 1, row = 4+i, sticky = tk.NW, padx = (90, 10), pady = (0, 5))
        widthstepone = len(subjectForScore[i])
        widthToAdd = widthstepone * 9
        label["Topic"] = tk.Label(dashboardImageLabel, text = ' - ' + str(topicForScore[i]), font = ('verdana', 8,), fg = GREY, bg = IVORY, justify = tk.RIGHT) 
        label["Topic"].grid(column = 1, row = 4+i, sticky = tk.NW, padx = (100+widthToAdd, 10), pady = (0, 5))
        label["Score"] = tk.Label(dashboardImageLabel, text = forScore[i], font = ('verdana', 8,), bg = IVORY, justify = tk.LEFT) 
        label["Score"].grid(column = 1, row = 4+i, sticky = tk.NW, padx = (90, 10), pady = (20, 20))

    subjects = [['bio', ['10/12', '15/30', '5/5']], ['chem', ['6/6', '6/7', '6/8']], ['maths', ['4/4', '16/30', '26/30']]]

    fig = Figure(figsize=(4,3), dpi=100)

    for subject in subjects:
        x = []
        y = []
        for score in subject[1]:
            for char in score:
                if char == '/':
                    a = score.index(char)
            num = int(score[:a])
            den = int(score[a+1:])
            percentage = int((num/den)*100)
            y.append(percentage)
        for i in range(len(y)):
            x.append(i+1)
        fig.add_subplot(111).plot(x, y, label = subject[0])
    

    fig.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=dashboardImageLabel)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(column = 1, row = 3, columnspan = 2, rowspan = 6, padx = (400,0), sticky = tk.E)   

    dashboardButton.config(fg = BLUE)
    ResourcesButton.config(fg = GREY)
    settingsButton.config(fg = GREY)


def resources(parentWindow):
    global dashboardButton 
    global ResourcesButton 
    global settingsButton
    global homeScreenFrame
    global resourcesSCF
    global HS

    destroyWindows()

    HS += 1
    
    resourcesSCF = tk.Frame(
        homeScreenFrame,
        bd = 0,
        bg = '#eeeeee'
    )

    resourcesSCF.pack(
        expand = 1, 
        fill = tk.BOTH, 
        side = 'top', 
        anchor = 'n'
    )

    currentDate = datetime.datetime.now()

    dateLabel = tk.Label(
        resourcesSCF,
        bd = 0,
        bg = '#eeeeee',
        fg = BLUE,
        text = currentDate.strftime("%x") + ' papers',
        font = ('verdana', 15)
    )

    dateLabel.grid(
        column = 1,
        row = 1,
        padx = (20, 20),
        pady = (20, 20)
    )

    count = 0
    for course in userData.studies:
        count += 1
        name = SUBJECTS[course.subject].upper()
        label = {}
        label["Question Paper"] = tk.Button(resourcesSCF, text = name, font = ('verdana', 12), padx = 20, pady = 20, command = lambda e = course.hash: examQuestionEntry(e)) #command = pass) #command to open paper
        label["Question Paper"].grid(column = 1, row = count, sticky = "NSEW")
        label["Done"] = tk.Button(resourcesSCF, text = 'Finished', font = ('verdana', 12), padx = 20, pady = 20,command = lambda e = course.hash: markSchemeEntry(e)) #command = pass) #command to open markscheme
        label["Done"].grid(column = 2, row = count, sticky = "NSEW")
        label["Grade"] = tk.Entry(resourcesSCF)
        label["Grade"].grid(column = 3, row = count, sticky = "NSEW")
        label["Submit"] = tk.Button(resourcesSCF, text = 'Submit Grade', font = ('verdana', 12), padx = 20, pady = 20,) #command = pass) #command to delete row and store result
        label["Submit"].grid(column = 4, row = count, sticky = "NSEW")

    dashboardButton.config(fg = GREY)
    ResourcesButton.config(fg = BLUE)
    settingsButton.config(fg = GREY)

def settings(parentWindow):
    global dashboardButton 
    global ResourcesButton 
    global settingsButton
    global homeScreenFrame
    global settingsFrame
    global HS

    destroyWindows()

    HS += 1
    
    settingsFrame = tk.Frame(
        parentWindow,
        bd = 0,
        bg = '#eeeeee'
    )

    settingsFrame.pack(
        expand = 1, 
        fill = tk.BOTH, 
        side = 'top', 
        anchor = 'n'
    )
    mainSettingsPage = tk.Frame(
        settingsFrame,
        bd = 0,
        bg = '#eeeeee'
    )

    mainSettingsPage.pack(
        expand = 1, 
        fill = tk.BOTH, 
        side = 'top', 
        anchor = 'n'
    )
    addCourseOption = tk.Button(
        mainSettingsPage,
        text = 'Add a course',
        font = ('verdana', 18),
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e=parentWindow : userCourseSelect(settingsFrame, 0,0, mainSettingsPage)
    )

    addCourseOption.grid(row = 0, column = 0)
    dashboardButton.config(fg = GREY)
    ResourcesButton.config(fg = GREY)
    settingsButton.config(fg = BLUE)

def tryDestruction(win):
    try:
        win.destroy()
        return True
    except:
        return False

def destroyWindows():
    tryDestruction(loginFrame)
    tryDestruction(createAccountFrame)
    tryDestruction(dashboardFrame)
    tryDestruction(settingsFrame)
    tryDestruction(resourcesSCF)

#~Files and Github~


"""Create a course from provided data"""
def createCourseFromData(subject, level, board, yearStart, topicList, topicMap, topicData):
    c = Course(subject, level, yearStart, board, getTopicObject(topicList, topicMap, topicData))
    return c



"""Create a course from a spec file"""
def createCourseFromFile(specfname):
    return parseSpec(specfname)



class Topic:
    def __init__(self, topicNumber, topicDesc, subTopics):
        self.topicNumber = topicNumber
        self.topicDesc = topicDesc
        self.subTopics = subTopics




 






class Course:
    def __init__(self, subject, level, year, board, topics, paperList = None):
        self.subject = subject
        self.board = board
        self.level = level
        self.topics = topics
        self.paperList = []
        self.yearStart = year
        self.hash = self.hashGen()

    def hashGen(self):
        return BOARDS[self.board][0] + str(len(BOARDS[self.board])) + str(LEVELS[self.level][0]) + str(len(LEVELS[self.level])) + str(SUBJECTS[self.subject][:3]) + str(len(SUBJECTS[self.subject])) + str(self.yearStart)[0] + "4"

    def addPaper(self, paper):
        self.paperList.append(paper)

    def addTopic(self, topic, keywords = []):
        t = Topic(topic, self.hash, keywords)
        self.topics.append(t)
        return t

    def __eq__(self, other):
        return self.hash == other.hash

    def __str__(self):
        return "Level: " + LEVELS[self.level] + "\nSubject: " + SUBJECTS[self.subject] + "\nBoard: " + BOARDS[self.board]




def examQuestionEntry(courseHash):
    take = tk.Tk()
    questionEntries = []
    entryFrame = tk.Frame(take)
    indexes = userData.getQuestionsToDo(courseHash)
    questionsToTake = [userData.questions[q] for q in indexes]
    row = 0
    for q in questionsToTake:
        questionLabel = tk.Label(entryFrame, text = q.question.question)
        questionEntry = tk.Entry(entryFrame)
        questionEntries.append(questionEntry)
        questionLabel.grid(row = row, colum = 0)
        questionEntry.grid(row=row, column = 1)
        row +=1
    submitButton = tk.Button(
        entryFrame,
        text = 'Submit',
        font = ('verdana', 18),
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e = questionEntries, f = indexes, g = take: submitAnswers(e, f, g)
    )
    submitButton.grid(row = row, column = 1)
    entryFrame.pack()

def submitAnswers(entries, indexes, win):
    entryData = [e.get() for e in entries]
    for i in range(len(entryData)):
        if entryData[i] != "":
            userData.questions[indexes[i]].submitAnswer(entryData[i])
    win.destroy()

def submitMarks(entries, indexes, win):
    entryData = [e.get() for e in entries]
    for i in range(len(entryData)):
        if entryData[i] != "":
            try:
                userData.questions[indexes[i]].markQuestion(int(entryData[i]))
            except:
                pass
    win.destroy()
            
    

def markSchemeEntry(courseHash):
    take = tk.Tk()
    markEntries = []
    entryFrame = tk.Frame(take)
    indexes = userData.getQuestionsToMark(courseHash)
    questionsToTake = [userData.questions[q] for q in indexes]
    row = 0
    for q in questionsToTake:
        questionLabel = tk.Label(entryFrame, text = "Question: " + q.question.question)
        answerLabel = tk.Label(entryFrame, text = "You answered: " + q.answer)
        markSchemeLabel = tk.Label(entryFrame, text = "The Markscheme says: " + q.question.markScheme)
        mEntryLabel = tk.Label(entryFrame, text = "Marks out of " + q.question.marks)
        marksEntry = tk.Entry(entryFrame)
        markEntries.append(marksEntry)
        questionLabel.grid(row = row, column = 0)
        row += 1
        answerLabel.grid(row = row, column = 0)
        row +=1
        markSchemeLabel.grid(row = row, column = 0)
        mEntryLabel.grid(row = row, column = 1)
        marksEntry.grid(row=row, column = 2)
        row +=2
    submitButton = tk.Button(
        entryFrame,
        text = 'Submit',
        font = ('verdana', 18),
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e = markEntries, f = indexes, g= take: submitMarks(e, f, g)
    )
    submitButton.grid(row = row, column = 1)
    entryFrame.pack()
    



class Scheduler:
    def __init__(self, userQuestionData, userCourseData, questionsperday):
        self.questionData = userQuestionData
        self.courseData = userCourseData
        self.questionsperday = questionsperday
        self.assignedQuestions = self.schedule()
        
    def schedule(self):
        courseHashes = [c.hash for c in self.courseData]
        courses = [downloadCourse(c) for c in courseHashes]
        allAssignedQuestions = []
        for course in courses:
            questionNumbers = len(course.paperList)
            print(questionNumbers, course.paperList, course.subject)
            assignedQuestions = []
            if questionNumbers != 0:
                while len(assignedQuestions) != self.questionsperday:
                    newQuestion = course.paperList[random.randint(0, questionNumbers)]
                    contains = False
                    for question in self.questionData:
                        if question == newQuestion:
                            contains = True
                    if not contains:
                        q = UserQuestion(newQuestion, course)
                        assignedQuestions.append(q)
                allAssignedQuestions += assignedQuestions
        return allAssignedQuestions

                        
                    
        



class UserQuestion:
    def __init__(self, question, courseHash):
        self.complete = False
        self.marked = False
        self.question = question
        self.courseHash = courseHash
        self.answer = ""
        self.marksAwarded = 0

    def __eq__(self, other):
        return self.question.question == other.question.question and self.courseHash == other.courseHash

    def submitAnswer(self, answer):
        self.answer = answer
        self.complete = True
        return self.question.markScheme
    
    def markQuestion(self, marks):
        if marks <= self.marksAwarded:
            self.marked = True
            self.marksAwarded = marks
            return True
        return False


class User:
    def __init__(self, username):
        self.username = username
        self.studies = []
        self.weakTopics = {}
        self.questions = []
        self.hoursPerDay = 0
        self.todaysSchedule = None
        self.lastScheduled = None

    def schedule(self):
        currentDate = datetime.date.today()
        if self.lastScheduled != currentDate:
            s = Scheduler(self.questions, self.studies, 3)
            self.questions += s.assignedQuestions
            self.lastScheduled = currentDate
            self.todaysSchedule = s
            setUserData()
            return True
        return False


    def addWeakTopic(self, course, topic):
        self.weakTopics[course].append(topic)

    def removeWeakTopic(self, course, topic):
        removeIndex = -1
        for i in range(len(self.weakTopics[course])):
            if self.weakTopics[course][i] == topic:
                removeIndex = i
        if removeIndex != -1:
            self.weakTopics[course].pop(removeIndex)
            return True
        return False
        
    def getQuestionsToDo(self, courseHash):
        questionsOut = []
        count = 0
        for q in self.questions:
            if q.courseHash == courseHash and not q.complete:
                questionsOut.append(count)
            count += 1
        return questionsOut
    
    def getQuestionsDone(self, courseHash):
        questionsOut = []
        count = 0
        for q in self.questions:
            if q.courseHash == courseHash and q.complete and q.marked:
                questionsOut.append(count)
            count += 1
        return questionsOut

    def getQuestionsToMark(self, courseHash):
        questionsOut = []
        count = 0
        for q in self.questions:
            if q.courseHash == courseHash and q.complete and not q.marked:
                questionsOut.append(count)
            count += 1
        return questionsOut


    def addCourse(self, course):
        self.studies.append(course)

    def dropCourse(self, course):
        removeIndex = -1
        for i in range(len(self.studies)):
            if self.studies[i] == course:
                removeIndex = i
        if removeIndex != -1:
            self.studies.pop(removeIndex)
            return True
        return False





"""Allows the user to select a course"""
def userCourseSelect(parentWindow, rowPos, colPos, mainSettingsFrame):
    try:
        mainSettingsFrame.destroy()
    except:
        pass    
    frame = ttk.Frame(parentWindow)
    frame.grid(row = rowPos, column = colPos)
    title = tk.Label(frame, text = "Select the course details: ", font = ("verdana", 25, "underline"))
    title.grid(row = 0, column  = 0)
    showLevelDropDown(frame)

def showLevelDropDown(parentWindow):
    global levelDropDown
    global levelLabel
    try:
        levelLabel.destroy()
        levelDropDown.destroy()
        subjectDropDown.destroy()
        subjectLabel.destroy()
        boardDropDown.destroy()
        boardLabel.destroy()
    except:
        pass
    levelDropDown = ttk.Combobox(parentWindow, values = LEVELS)
    levelLabel = tk.Label(parentWindow, text = "Level: ")
    levelDropDown.bind("<<ComboboxSelected>>", lambda e, f=parentWindow: showSubjectDropDown(f, levelDropDown.current()))
    levelDropDown.grid(row = 1, column = 2)
    levelLabel.grid(row = 1, column = 1)


def showSubjectDropDown(parentWindow, selectedLevel):
    global subjectDropDown
    global subjectLabel
    try:
        subjectDropDown.destroy()
        subjectLabel.destroy()
        boardDropDown.destroy()
        boardLabel.destroy()
    except:
        pass
    subjects = getSubjects(selectedLevel)
    subjects = [SUBJECTS[s].upper() for s in subjects]
    subjectDropDown = ttk.Combobox(parentWindow, values = subjects)
    subjectLabel = tk.Label(parentWindow, text = "Subject: ")
    subjectDropDown.bind("<<ComboboxSelected>>", lambda e, f=parentWindow, g = selectedLevel, h = subjects: showBoardDropDown(f, g, SUBJECTS.index(h[subjectDropDown.current()].lower())))
    subjectDropDown.grid(row = 2, column = 2)
    subjectLabel.grid(row = 2, column =1)

    
def showBoardDropDown(parentWindow, selectedLevel, selectedSubject):
    global boardDropDown
    global boardLabel
    try:
        boardDropDown.destroy()
        boardLabel.destroy()
    except:
        pass
    boards = getBoards(selectedLevel, selectedSubject)
    boards = [BOARDS[b] for b in boards]
    boardDropDown = ttk.Combobox(parentWindow, values = boards)
    boardLabel = tk.Label(parentWindow, text = "Exam board: ")
    boardDropDown.bind("<<ComboboxSelected>>", lambda e, f = parentWindow, g = selectedLevel, h = selectedSubject, i = boards: showAddCourseButton(f,g,h,BOARDS.index(i[boardDropDown.current()])))
    boardDropDown.grid(row = 3, column = 2)  
    boardLabel.grid(row = 3, column = 1)


def showAddCourseButton(parentWindow, selectedLevel, selectedSubject, selectedBoard):
    global addCourseButton
    try:
        addCourseButton.destroy()
    except:
        pass
    addCourseButton = tk.Button(
        parentWindow,
        text = 'Add',
        font = ('verdana', 18),
        bg = IVORY,
        fg = '#555555',
        activebackground = '#D1D4E7',
        bd = 0,
        command = lambda e=parentWindow, f = selectedLevel, g = selectedSubject, h = selectedBoard : addCourse(e,f,g,h)
    )
    addCourseButton.grid(row = 4, column = 1)

    
"""Search for a course"""
def searchCourses(level, subject, board):
    now = datetime.datetime.now()
    year = now.year
    hashes = allCourses.keys()
    for i in range(year, 1980, -1):
        c = Course(subject, level, year, board, {})
        if c.hash in hashes:
            return allCourses[c.hash]
    return -1
            

        
"""Add a course to a user's repetoire"""
def addCourse(parentWindow, selectedLevel, selectedSubject, selectedBoard):
    c = searchCourses(selectedLevel, selectedSubject, selectedBoard) 
    try:
        x = c == -1
        displayCourseErrorMessage(parentWindow)
    except:
        userData.addCourse(c) 
        setUserData()
    parentWindow.destroy()
    homeScreen(UI)




"""Creates a user"""
def createUser(username):
    u = User(username)
    pickleData(u, username + ".dat")
    uploadFile(username + ".dat", "users")
    return u


"""Gets User Data into the global variable"""
def getUserData(username):
    global userData
    success, errorCode = download(username + ".dat", "users")
    if success:
        userData = unpickle(username + ".dat")
        return True
    else:
        if errorCode == Errors().UserDoesntExistError:
            userDataTemp = createUser(username)
            if userDataTemp == Errors().FileNotFoundError:
                return False
            userData = userDataTemp
            return True
        else:
            userDataTemp = unpickle(username + ".dat")
            if userDataTemp == Errors().FileNotFoundError:
                return False
            userData = userDataTemp
            return True

def setUserData():
    global userData
    username = userData.username
    pickleData(userData, username + ".dat")
    uploadFile(username + ".dat", "users")

def uploadCourse(c):
    pickleData(c, c.hash + ".dat")
    uploadFile(c.hash + ".dat", "courses")

def downloadCourse(hash):
    download(hash + ".dat", "courses")
    return unpickle(hash + ".dat")

def uploadCourseList():
    pickleData(allCourses, "Course Torrent.dat")
    uploadFile("Course Torrent.dat", "data")

def downloadCourseList():
    download("Course Torrent.dat", "data")
    return unpickle("Course Torrent.dat")

#############################
##############################
###############################
################################
#################################
##################################


def getSubjects(level):
    subjects = []
    myCourses = [s.hash for s in userData.studies]
    for c in allCourses.values():
        if c.level == level:
            if c.hash not in myCourses:
                subjects.append(c.subject)
    return subjects

def getBoards(level, subject):
    boards = []
    myCourses = [s.hash for s in userData.studies]
    for c in allCourses.values():
        if c.level == level and c.subject == subject:
            if c.hash not in myCourses:
                boards.append(c.board)
    return boards


class Errors(RuntimeError):
    def __init__(self):
        self.NoInternetError = "Please check your internet connection"
        self.UserDoesntExistError = "User data file missing"
        self.FileNotFoundError = "Specified file doesn't exist"


####SPEC PARSE


def getTopicObject(topicList, subTopicTree, topicData):
    topicMap = {}
    count = 0
    for key in subTopicTree.keys():
        subTopicList = []
        for skey in subTopicTree[key].keys():
            subsubTopicList = []
            for sskey in subTopicTree[key][skey]:
                t = Topic(sskey, topicData[sskey], [])
                subsubTopicList.append(t)
            t = Topic(skey, topicData[skey], subsubTopicList)
            subTopicList.append(t)
        t = Topic(key, topicData[key], subTopicList)
        topicMap[topicList[count]] = t
        count += 1
    return topicMap




            


def clean(text):
    text = text.replace("™", "'")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("˜", "fi")
    text = text.replace("\\n", " ")
    text = text.replace("\\n", " ")
    for i in range(20, 1, -1):
        replacetxt = ""
        for j in range(i):
            replacetxt += " "
        text = text.replace(replacetxt, " ") 
    return text

def decryptPdf(fname):
    with pikepdf.open(fname, password='') as pdf:
        num_pages = len(pdf.pages)
        del pdf.pages[-1]
        pdf.save("temp.pdf")
    os.remove(fname)
    os.rename("temp.pdf", fname)
    
def pdf2text(fname):
    text = ""
    pages = []
    f = open(fname, 'rb')
    pdfReader = p2.PdfFileReader(f) 
    if pdfReader.isEncrypted:
        f.close()
        decryptPdf(fname)       
        f = open(fname, 'rb')
    cv = Converter(fname)
    cv.convert("temp.docx", start=0, end=None)
    cv.close()
    try:
        shutil.rmtree("tempImages")
    except:
        pass
    os.mkdir("tempImages")
    text = clean(docx2txt.process("temp.docx", 'tempImages'))
    os.remove("temp.docx")
    return text, pages
    
def getSubTopicTree(array):
    currentMainTopic = None
    currentSubTopic = None
    tree = {}
    for t in array:
        dps = count(t, ".")
        if dps == 1:
            currentMainTopic = t
            tree[currentMainTopic] = {}
        elif dps == 2:
            currentSubTopic = t
            tree[currentMainTopic][currentSubTopic] = []
        else:
            tree[currentMainTopic][currentSubTopic].append(t)
    return tree



def getContentsPage(text):
    findPhrase = " Contents 1 "
    start = text.find(findPhrase)
    startChapter = ""
    for i in range(start + len(findPhrase), len(text)):
        try:
            int(text[i])
            startChapter = text[start + len(findPhrase):i]
            break
        except:
            pass
    end = text.find("1 " + startChapter, start + len(findPhrase))
    return text[start + len(findPhrase):end], end

def findNumRange(text, decPoint):
    start = -1
    end = -1
    for i in range(decPoint, len(text)):
        try:
            int(text[i])
        except:
            if text[i] == " ":
                end = i + 1
                break
    for i in range(decPoint, -1, -1):
        try:
            int(text[i])
        except:
            if text[i] == " ":
                start = i
                break
    if start == -1:
        start = 0
    if end == -1:
        end = len(text)
    return start, end

def parseByNumber(text):
    startLocs = []
    endLocs = []
    for i in range(len(text)):
        try:
            if text[i] == ".":
                int(text[i-1])
                int(text[i+1])
                start, end = findNumRange(text, i)
                if len(startLocs) == 0:
                    startLocs.append(end)
                else:
                    startLocs.append(end)
                    endLocs.append(start)
        except:
            pass
    endLocs.append(len(text) - 1)
    arr = []
    for i in range(len(startLocs)):
        arr.append(text[startLocs[i] : endLocs[i]])
    newArr = []
    for t in arr:
        newArr.append(cleanPageNums(t))
    return newArr

def cleanPageNums(text):
    return text[:text.rfind(" ")]

def getTopics(text):
    sLoc = text.find("Subject content ") + len("Subject content ")
    eLoc = text.find("Scheme of assessment ", sLoc)
    topics = parseByNumber(text[sLoc:eLoc])
    return topics

def formulateNextTopic(lastTopic):
    lastTopic = lastTopic.replace(" ", "")
    lastDP = lastTopic.rfind(".") + 1
    return " " + lastTopic[:lastDP] + str(int(lastTopic[lastDP:]) + 1) + " "

def getLevelUpTopic(currentTopic):
    currentTopic = currentTopic.replace(" ", "")
    lastDP = currentTopic.rfind(".")
    return " " + currentTopic[:lastDP] + " "

def addLevelBelowTopic(currentTopic):
    currentTopic = currentTopic.replace(" ", "")
    return " " + currentTopic + ".1 "

def count(string, char):
    num = 0
    for c in string:
        if c == char:
            num += 1
    return num

def parseTopics(text, topics):
    topicData = {}
    currentTopic = " 3.1 "
    lastTopic = " 3.1 "
    startLoc = 0
    endOfQuestions = False
    finalLoc = text.rfind(" 3.")
    while not endOfQuestions:
        loc = text.find(currentTopic, startLoc)
        if loc == finalLoc:
            topicData[lastTopic] = text[startLoc + len(lastTopic) : loc]
            topicData[currentTopic] = text[loc + len(currentTopic) :]
            endOfQuestions = True
            break
        if loc != -1:
            topicData[lastTopic] = text[startLoc + len(lastTopic) : loc]
            lastTopic = currentTopic
            startLoc = loc
            if count(currentTopic, ".") < 3:
                currentTopic = addLevelBelowTopic(currentTopic)
            else:
                currentTopic = formulateNextTopic(currentTopic)
        else:
            if count(currentTopic, ".") > 1:
                upTopic = getLevelUpTopic(currentTopic)
                currentTopic = formulateNextTopic(upTopic)
            else:
                topicData[currentTopic] = text[startLoc + len(currentTopic) :]
                endOfQuestions = True
                break
    return topicData



def determineLevel(text):
    loc = text.find("AS AND A-LEVEL")
    if loc == -1:
        loc = text.find("GCSE")
        if loc == -1:
            return LEVELS.index("11+"), loc + len("11+") + 1
        else:
            return LEVELS.index("GCSE"), loc + len("GCSE") + 1
    else:
        return LEVELS.index("AS AND A-LEVEL"), loc + len("AS AND A-LEVEL") + 1


def getYear(text):
    loc = text.find("For teaching from")
    for i in range(loc, len(text)):
        try:
            int(text[i])
            return int(text[i:i+4])
        except:
            pass
    return 2000

def getSubject(text):
    loc = text.find("(")
    nloc = text[:loc - 1].rfind(" ")
    try:
        return SUBJECTS.index(text[:nloc].lower())
    except:
        SUBJECTS.append(text[:nloc].lower())
        uploadTypesLists()
        return len(SUBJECTS) -1 


"""Parse a spec file"""
def parseSpec(fname):
    board = BOARDS.index("AQA")
    text, pages = pdf2text(fname)
    level, loc = determineLevel(text[:50])
    subject = getSubject(text[loc:200])
    year = getYear(text[loc:200])
    contentsPages, end = getContentsPage(text)
    topicList = getTopics(contentsPages)
    topicStart = text.rfind("Subject content")
    topicEnd = text.find("Scheme of assessment", topicStart)
    topicData = parseTopics(text[topicStart : topicEnd], topicList)
    topicMap = {}
    subTopicTree = getSubTopicTree(topicData.keys())
    return Course(subject, level, year, board, getTopicObject(topicList, subTopicTree, topicData))





#######FILES AND GITHUB





def uploadFile(fname, directory):
    try:
        g = Github("58f6651a4e7ab3a7d6d863991e1a84a187d35718")
        user = g.get_user()
        repo = user.get_repo("kacademy")
        all_files = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
        with open(fname, 'rb') as file:
            content = file.read()
        # Upload to github
        git_prefix = directory
        git_file = git_prefix + "/" + fname
        if git_file in all_files:
            contents = repo.get_contents(git_file)
            repo.update_file(contents.path, "Data Upload", content, contents.sha, branch="main")
        else:
            repo.create_file(git_file, "Data Upload", content, branch="main")
        return True
    except:
        return Errors().NoInternetError


def download(fname, directory):
    try:
        g = Github("58f6651a4e7ab3a7d6d863991e1a84a187d35718")
        user = g.get_user()
        repo = user.get_repo("kacademy")
    except:
        return False, Errors().NoInternetError
    try:
        contents = repo.get_contents(directory + "/" + fname, ref="main")
        file_content = repo.get_contents(urllib.parse.quote(contents.path), ref="main")
        urllib.request.urlretrieve(file_content.download_url, fname)
        return True, None
    except:
        return False, Errors().UserDoesntExistError


def pickleData(o, fname):
    with open (fname, 'wb') as f:
        pickle.dump(o, f)

def unpickle(fname):     
    try:
        with open(fname, 'rb') as f:
            dat = pickle.load(f)
        return dat
    except:
        return Errors().FileNotFoundError



def uploadTypesLists():
    types = [LEVELS, BOARDS, SUBJECTS]
    pickleData(types, "types.dat")
    uploadFile("types.dat", "data")


def downloadTypesLists():
    global LEVELS
    global BOARDS
    global SUBJECTS
    download("types.dat", "data")
    types = unpickle("types.dat")
    LEVELS = types[0]
    BOARDS = types[1]
    SUBJECTS = types[2]



class Question:
    def __init__(self, questionNumber, rawquestion):
        self.question = None
        self.markScheme = None
        self.marks = None
        self.fullqNum = questionNumber
        self.images = []
        self.qNum, self.subqNum = self.getQuestionNums(questionNumber)
        self.parseQuestion(rawquestion)

    def parseQuestion(self, rawQ):
        pass

    def getQuestionNums(self, qNum):
        return None, None



class EDEXCELQuestion(Question):
    def __init__(self, startPage, endPage, startLoc, endLoc, questionNumber, question, currentMainQ, currentSubQ):
        super().__init__(startPage, endPage, startLoc, endLoc, questionNumber, question)
        self.subsubqNum = questionNumber
        self.qNum = currentMainQ
        self.subqNum = currentSubQ
        self.question = self.question.replace("...", "")
        self.fullqNum = self.getFullQNum()

    def getFullQNum(self):
        if self.subsubqNum is None:
            if self.subqNum is None:
                return str(self.qNum)
            return str(self.qNum) + self.subqNum
        return str(self.qNum) + self.subqNum + self.subsubqNum

class AQAQuestion(Question):
    def __init__(self, questionNumber, question):
        super().__init__(questionNumber, question)


    def getImage(self, figureNum):
        figureNum = 1
        with open("tempImages\\image" + str(resourceMap["Figure " + str(figureNum)]) + ".png", 'rb') as f:
            image = f.read()
        return image

    def getTable(self, tableNum):
        tableNum = 1
        with open("tempImages\\image" + str(resourceMap["Figure " + str(tableNum)]) + ".png", 'rb') as f:
            image = f.read()
        return image

    def clean(self, rawQ):
        loc = 0
        rawQ = rawQ.replace("Answer all questions in the spaces provided. ", "")
        while loc != -1:
            text = " Do not write outside the box "
            loc = rawQ.find(text)
            if loc != -1:
                firstIntFound = False
                for i in range(loc - 1, -1, -1):
                    text = rawQ[i] + text
                    try:
                        int(rawQ[i])
                        firstIntFound = True
                    except:
                        if firstIntFound:
                            break
                rawQ = rawQ.replace(text, "")
        loc = 0
        while loc != -1:
            loc = rawQ.find("*", loc + 1)
            if loc != -1:
                try:
                    int(rawQ[loc+1:loc+3])
                    if rawQ[loc + 3] == "*":
                        rawQ = rawQ[:loc] + rawQ[loc + 4 :]
                        loc = loc + 4
                except:
                    try:
                        int(rawQ[loc+1:loc + 2])
                        if rawQ[loc + 2] == "*":
                            rawQ = rawQ[:loc] + rawQ[loc + 3 :]
                            loc = loc + 3
                    except:
                        pass

        newQNum = ""
        for x in self.fullqNum:
            newQNum += x
            newQNum += " "
        newQNum = newQNum[:-1]
        qNumLoc = rawQ.find(newQNum)
        rawQ = rawQ[qNumLoc + len(newQNum):]
        sMarkloc = rawQ.find("[") + 1
        eMarkloc = rawQ.find(" marks", sMarkloc)
        if eMarkloc == -1:
            eMarkloc = rawQ.find(" mark", sMarkloc)
        if sMarkloc == -1 or eMarkloc == -1:
            return rawQ, None
        return rawQ[:sMarkloc - 1], int(rawQ[sMarkloc:eMarkloc])


    def parseQuestion(self, rawQ):
        imagesAdded = []
        rawQ, self.marks = self.clean(rawQ)
        loc = 0
        while loc != -1:
            loc = rawQ.find("Figure ", loc + len("Figure "))
            if loc != -1:
                sLoc = loc + 7
                try:
                    figure = int(rawQ[sLoc : sLoc + 2])
                except:
                    figure = int(rawQ[sLoc:sLoc + 1])
                if figure not in imagesAdded:
                    self.images.append(self.getImage(figure))
                    imagesAdded.append(figure)
        loc = 0
        while loc != -1:
            loc = rawQ.find("Table ", loc + len("Table "))
            if loc != -1:
                sLoc = loc + 6
                try:
                    figure = int(rawQ[sLoc : sLoc + 2])
                except:
                    figure = int(rawQ[sLoc:sLoc + 1])
                if figure not in imagesAdded:
                    self.images.append(self.getTable(figure))
                    imagesAdded.append(figure)
        self.question = rawQ


    def getQuestionNums(self, fullqNum):
        qNum = None
        subqNum = None
        pointSep = 0
        for i in range(len(fullqNum)):
            if fullqNum[i] == ".":
                pointSep = i
                break

        if pointSep == 0:
            try:
                qNum = int(fullqNum)
            except:
                pass
            subqNum = None
        else:
            try:
                qNum = int(fullqNum[:pointSep])
                subqNum = int(fullqNum[pointSep+1:])
            except:
                pass
        return qNum, subqNum

def formulateAQASubQuestion(llq, lsq):
    llqs = str(llq)
    lsqs = str(lsq)
    if len(llqs) == 1:
        llqs = "0" + llqs
    outQ = llqs + "." + lsqs
    newOutQ = ""
    for c in outQ:
        newOutQ += c
        newOutQ += " "
    return newOutQ[:-1]


def formulateAQAQuestion(llq):
    llqs = str(llq)
    if len(llqs) == 1:
        llqs = "0" + llqs
    newOutQ = ""
    for c in llqs:
        newOutQ += c
        newOutQ += " "
    return newOutQ[:-1]

def replacePaperCode(text):
    loc = text.rfind("IB/M/")
    slashCount = 0
    for i in range(loc, len(text)):
        if text[i] == "/":
            slashCount += 1
        if slashCount == 4:
            paperCode = text[loc:i+2]
            break
    return text.replace(paperCode, "")


def between(number, lb, ub):
    return number <= ub and number >= lb


def cleanImages():
    path, dirs, files = next(os.walk("tempImages"))
    fileCount = len(files)
    removeImages = []
    for i in range(1, fileCount):
        filepath = "tempImages\\image" + str(i) + ".png"
        with Image.open(filepath) as img:
            width, height = img.size
        file_stats = os.stat(filepath)
        size = file_stats.st_size
        if between(width, 1500, 1700) and between(height, 2000, 2200):
            removeImages.append(i)
        if size < (30 * 1024):
            removeImages.append(i)
    removeImages.reverse()
    for removeImage in removeImages:
        filepath = "tempImages\\image" + str(removeImage) + ".png"
        os.remove(filepath)
        for i in range(removeImage + 1, fileCount):
            os.rename("tempImages\\image" + str(i) + ".png", "tempImages\\image" + str(i - 1) + ".png")
        fileCount -= 1


def getResourceMap(text):
    global resourceMap
    resourceMap = {}
    tempMap = {}
    loc = 0
    currentFigure = 1
    while loc != -1:
        loc = text.find("Figure " + str(currentFigure), loc)
        if loc != -1:
            tempMap[loc] = "Figure " + str(currentFigure)
            currentFigure += 1
    loc = 0
    currentTable = 1
    while loc != -1:
        loc = text.find("Table " + str(currentTable), loc)
        if loc != -1:
            tempMap[loc] = "Table " + str(currentTable)
            currentTable += 1
    count = 1
    for loc in tempMap.keys():
        resourceMap[tempMap[loc]] = count
        count += 1
    


    

def AQAquestionParse(text):
    text = replacePaperCode(text)
    lastLargeQ = 1
    lastSubQ = 1
    questions = {}
    lastQuestion = "01"
    lastLoc = text.find(" 0 1 ")
    endOfTest = False
    while not endOfTest:
        question = formulateAQASubQuestion(lastLargeQ, lastSubQ)
        loc = text.find(question, lastLoc)
        if loc == -1:
            question = formulateAQAQuestion(lastLargeQ + 1)
            loc = text.find(question, lastLoc)
            if loc == -1:
                questions[lastQuestion] = text[lastLoc:]
                endOfTest = True
                break
            else:
                questions[lastQuestion] = text[lastLoc:loc]
                lastQuestion = question.replace(" ", "")
                lastLoc = loc
                lastLargeQ += 1
                lastSubQ = 1
                
        else:
            questions[lastQuestion] = text[lastLoc:loc]
            lastQuestion = question.replace(" ", "")
            lastSubQ += 1
            lastLoc = loc
    questionObjects = []
    cleanImages()
    getResourceMap(text)
    for q in questions.keys():
        questionObjects.append(AQAQuestion(q, questions[q]))
    return questionObjects


def questionParse(text, board):
    if board == "AQA":
        return AQAquestionParse(text)
    elif board == "EDX":
        return EDXquestionParse(text)



def removeDuplicates(l):
    newL = []
    for t in l:
        if t not in newL:
            newL.append(t)
    return newL

    
def getAllFileNames(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".pdf"):
            files.append(os.path.join(file))
    return files

class Paper:
    def __init__(self, file):
        self.fname = file
        self.board = None
        self.year = None
        self.month = None
        self.day = None
        self.pCode = None
        self.sCode = None
        self.pType = None
        self.MARKSCHEME = "MS"
        self.QUESTIONPAPER = "QP"
        self.INSERT = "INS"
        self.AQA = "AQA"
        self.EDEXCEL = "EDEX"


    def getPopualtionState(self):
        return(self.month is not None) and (self.year is not None) and (self.pType is not None) and (self.sCode is not None) and (self.pCode is not None)

    def __eq__(self, other):
        return self.year == other.year and self.pCode == other.pCode and self.sCode == other.sCode and self.sameSeries(other) and self.board == other.board

    def sameSeries(self, other):
        x = int(other.month)
        if self.month == 1:
            return x == 1 or x == 2 or x == 12 or x == 11 or x == 3
        if self.month == 12:
            return x == 1 or x == 12 or x == 11 or x == 10 or x == 2
        return int(self.month) >= x - 2 and int(self.month) <= x + 2

class EDEXPaper(Paper):
    def __init__(self, file):
        super().__init__(file)
        self.populate(file)
        self.board = self.EDEXCEL
        self.populated = self.getPopualtionState()
        

    def populate(self, file):
        lastUnderScore = 0
        parseNumber = 0
        for i in range(len(file)):
            if file[i:i+1] == "_":
                x = file[lastUnderScore:i]
                if parseNumber == 0: 
                    self.sCode = x
                elif parseNumber == 1: 
                    self.pCode = x
                elif parseNumber == 2: 
                    if x == "rms":
                        self.pType = self.MARKSCHEME
                    elif x == "que":
                        self.pType = self.QUESTIONPAPER
                    else:
                        self.pType = None
                lastUnderScore = i + 1
                parseNumber += 1
        fullDate = file[lastUnderScore:]
        self.year = fullDate[:4]
        self.month = fullDate[4:6]
        self.day = fullDate [6:8]



class AQAPaper(Paper):
    def __init__(self, file):
        super().__init__(file)
        self.populate(file)
        self.board = self.AQA
        self.populated = self.getPopualtionState()
        
    
    def populate(self, file):
        if "QP" in file:
            self.pType = self.QUESTIONPAPER
        elif "INS" in file:
            self.pType = self.INSERT
        elif "MS" in file or "-v" in file or "final" in file:
            self.pType = self.MARKSCHEME
        else:
            self.pType = None
        if file[:4] == "AQA-":
            self.sCode = file[4:8]
            self.pCode = file[9:10]
        else:
            self.sCode = file[:4]
            self.pCode = file[5:6]
        if self.pType == self.MARKSCHEME:
            months = monthNumberMap.keys()
            for i in range(1, len(file)):
                if file[i:i+3].lower() in months and file[i-1] == "-" and (file[i+5] == "-" or file[i+5] == "."): 
                    self.month = str(monthNumberMap[file[i:i+3].lower()])
                    self.year = file[i+3:i+5]
                    self.day = None
        if self.pType == self.QUESTIONPAPER:
            months = monthNumberMap.keys()
            for i in range(3, len(file)):
                if file[i:i+3].lower() in months and file[i-3] == "-" and (file[i+5] == "-" or file[i+5] == "."): 
                    self.month = str(monthNumberMap[file[i:i+3].lower()])
                    self.year = file[i+3:i+5]
                    self.day = file[i-2:i]
                elif file[i:i+3].lower() in months and file[i-2] == "-" and (file[i+5] == "-" or file[i+5] == "."): 
                    self.month = str(monthNumberMap[file[i:i+3].lower()])
                    self.year = file[i+3:i+5]
                    self.day = file[i-1:i]

        

def isAQAPaper(file):
    months = monthNumberMap.keys()
    if " " in file:
        return False
    if "-" not in file:
        return False
    containsMonth = False
    for month in months:
        if month in file.lower():
            containsMonth = True
    if not containsMonth:
        return False
    if file[:4] == "AQA-":
        try:
            int(file[4:8])
            int(file[9:10])
        except:
            return False
    else:
        try:
            int(file[:4])
            int(file[5:6])
        except:
            return False
    return True

def isEdexcelPaper(file):
    months = monthNumberMap.keys()
    if " " in file:
        return False
    if "_" not in file:
        return False
    containsMonth = False
    try:
        int(file[0])
    except:
        return False
    
    try:
        int(file[1])
        return False
    except:
        pass
    try:
        int(file[2])
        return False
    except:
        pass
    try:
        int(file[3])
    except:
        return False

    return True






def parseFiles(files):
    fmap = {}
    papers = []
    for file in files:
        if isEdexcelPaper(file):
            p = EDEXPaper(file)
            if p.populated:
                papers.append(p)
        elif isAQAPaper(file):
            p = AQAPaper(file)
            if p.populated:
                papers.append(p)
    for paper1 in papers:
        if paper1.fname not in fmap.keys() and paper1.fname not in fmap.values():
            for paper2 in papers:
                if paper2.fname not in fmap.keys() and paper2.fname not in fmap.values():
                    if paper1 == paper2:
                        if paper1.pType == paper1.MARKSCHEME and paper2.pType == paper2.QUESTIONPAPER:
                            fmap[paper2.fname] = paper1.fname
                            break
                        elif paper2.pType == paper2.MARKSCHEME and paper1.pType == paper1.QUESTIONPAPER:
                            fmap[paper1.fname] = paper2.fname
                            break
    return fmap



def getBoard(paper):
    if isAQAPaper(paper):
        return "AQA"
    if isEdexcelPaper(paper):
        return "EDX"

def getMarkScheme(fname, questionNums):
    text, pages = pdf2text(fname)
    text = text.replace(" ", "")
    msMap = {}
    prevPos = len(text)
    for i in range(len(questionNums) -1, -1, -1):
        if len(questionNums[i]) != 2:
            pos = text.rfind(questionNums[i], prevPos)
            if pos != -1:
                msMap[questionNums[i]] = text[pos:prevPos]
                prevPos = pos
    return msMap



def getPaper(fname):
    p = Path(fname)
    fmap = parseFiles(getAllFileNames(p.parent))
    msName = fmap[fname]
    board = getBoard(fname)
    text, pages = pdf2text(fname)
    questions = questionParse(text, board)
    qNums = [q.fullqNum for q in questions]
    msMap = getMarkScheme(msName, qNums)
    for q in questions:
        try:
            q.markScheme = msMap[q.fullqNum]
        except:
            pass
    return questions

def addQuestions(questions, courseHash):
    c = downloadCourse(courseHash)
    c.paperList += questions
    uploadCourse(c)

def main():
    global allCourses
    allCourses = downloadCourseList()
    downloadTypesLists()
    UI = start()
    login(UI)
    UI.mainloop()

main()
