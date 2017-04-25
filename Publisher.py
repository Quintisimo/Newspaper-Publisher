
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n9703578
#    Student name: Quintus Cardozo
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  Publish Your Own Periodical
#
#  In this task you will combine your knowledge of HTMl/XML mark-up
#  languages with your skills in Python scripting, pattern matching
#  and Graphical User Interface design and development to produce a
#  useful application for publishing a customised newspaper or
#  magazine on a topic of your own choice.  See the instruction
#  sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements that were used in our sample
# solution.  You should be able to complete this assignment using
# these functions only.

# Import the function for opening a web document given its URL.
from urllib import urlopen

# Import the function for finding all occurrences of a pattern
# defined via a regular expression.
from re import findall

# A function for opening an HTML document in your operating
# system's default web browser. We have called the function
# "webopen" so that it isn't confused with the "open" function
# for writing/reading local text files.
from webbrowser import open as webopen

# An operating system-specific function for getting the current
# working directory/folder.  Use this function to create the
# full path name to your publication file.
from os import getcwd

# An operating system-specific function for 'normalising' a
# path to a file to the path naming conventions used on this
# platform.  Apply this function to the full name of your
# publication file so that your program will work on any
# operating system.
from os.path import normpath

# Import the standard Tkinter functions.
from Tkinter import *

# Import the SQLite functions.
from sqlite3 import *

# Import the date/time function.
from datetime import datetime

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the published newspaper or magazine. To simplify marking,
# your program should publish its results using this file name.
file_name = 'publication.html'
newspaper_generator=Tk()
newspaper_generator.title('The Freedom Times')

#FIRST SECTION
first_section=Label(newspaper_generator, text='Choose you news topic:', font='-weight bold -size 12')
first_section.place(x=10,y=0)

top_story_variable=IntVar()
most_read_variable=IntVar()
politics_headlines_variable=IntVar()
money_headlines_variable=IntVar()
tech_headlines_variable=IntVar()
travel_news_variable=IntVar()

#Print button is disabled when no checkbutton is selected
def print_button_enabled():
    if top_story_variable.get()==1 or most_read_variable.get()==1 or politics_headlines_variable.get()==1 \
    or money_headlines_variable.get()==1 or tech_headlines_variable.get()==1 or travel_news_variable.get()==1:
        
        print_button.configure(state=NORMAL)
    else:
        print_button.configure(state=DISABLED)

topics_frame=Frame(newspaper_generator)
topics_frame.grid(row=0, column=0, pady=(25,5), padx=40)

top_story=Checkbutton(topics_frame, text='Top Story', variable=top_story_variable, command=print_button_enabled)
top_story.grid(row=1, column=0, sticky='w', padx=(0,20))

most_read=Checkbutton(topics_frame, text='Most Read', variable=most_read_variable, command=print_button_enabled)
most_read.grid(row=1, column=1, sticky='w')

politics_headlines=Checkbutton(topics_frame, text='Politics', variable=politics_headlines_variable, command=print_button_enabled)
politics_headlines.grid(row=2, column=0, sticky='w', padx=(0,20))

money_headlines=Checkbutton(topics_frame, text='Money', variable=money_headlines_variable, command=print_button_enabled)
money_headlines.grid(row=2, column=1, sticky='w')

tech_headlines=Checkbutton(topics_frame, text='Technology', variable=tech_headlines_variable, command=print_button_enabled)
tech_headlines.grid(row=3, column=0, sticky='w', padx=(0,20))

travel_news=Checkbutton(topics_frame, text='Travel', variable=travel_news_variable, command=print_button_enabled)
travel_news.grid(row=3,column=1, sticky='w')

#SECOND SECTION
second_section=Label(newspaper_generator, text='Generate Newspaper:', font='-weight bold -size 12')
second_section.place(x=10, y=110)

#Print button function
def generate_paper():
    print_button.configure(state=DISABLED)#print button is disabled so that the program cannot be interrupted while it runs

    progress_box.configure(state=NORMAL)
    progress_box.delete(1.0,END)#all text in the progressbox is deleted

    progress_box.insert(INSERT, 'GENERATING BLANK NEWSPAPER...\n')
    progress_box.update()

    newspaper=open(file_name,'w')
    newspaper.write('<html>\n\n')
    newspaper.write('<head>\n')
    newspaper.write('<title>The Freedom Times</title>\n')
    newspaper.write('<style>body {color:white; background-image: url("https://goo.gl/oPqZte"); background-size: cover}</style>')
    newspaper.write('</head>\n\n<body>\n\n')

    #Generating Masthead
    progress_box.insert(INSERT, 'GENERATING MASTHEAD...\n')
    progress_box.update()

    newspaper.write('<!--MASTHEAD-->\n')
    newspaper.write('<img src="https://goo.gl/KDYa2g" width="150" height="150" align="left">\n')
    newspaper.write('<h1 style="margin-bottom:-15">The Freedom Times</h1>\n')
    newspaper.write('<p>&nbsp;Your place to get informed</p>\n')
    newspaper.write('<hr size="8" color="red">\n\n')
    newspaper.write('<h2 style="margin-top:80"><!--Blank Space--></h2>\n\n')
    newspaper.write('<!--NEWS ARTICLES-->\n')

    progress_box.insert(INSERT, 'SEARCHING FOR NEWS STORIES...\n')
    progress_box.update()

    #List variable to enter data into database
    global database_link_datetime
    database_link_datetime=[]

    #Function to perform regex and generate article with html tags
    def news_scraper(url):
        web_page=urlopen(url).read()
        article_headline=findall('<title><!\[CDATA\[(.*)\]\]></title>', web_page)[0]
        article_image=findall('http://a.abcnews.com/images/[A-Za-z]*/[A-za-z0-9]*384.jpg', web_page)[0]
        article_description=findall('<description><!\[CDATA\[(.*)\]\]></description>', web_page)[0]
        global article_link
        article_link=findall('<link><!\[CDATA\[(.*)\]\]></link>', web_page)[0]
        global date_time
        date_time=str(datetime.now())[:19] #rounding time to seconds
        article_dateandtime=findall('<pubDate>(.*)</pubDate>', web_page)[0]

        newspaper.write('<img src="' + article_image + '" align="left" hspace="30">\n')
        newspaper.write('<h3>' + article_headline + '</h3>\n')
        newspaper.write('<p>' + article_description + '</p>\n')
        newspaper.write('<p>' + article_link + '</p>\n')
        newspaper.write('<p style="margin-bottom:200">' + article_dateandtime + '</p>\n')
        newspaper.write('<hr size="4" color="purple">\n\n')

        #Buttons activated after newspaper is generated
        read_button.configure(state=NORMAL)
        record_button.configure(state=NORMAL)

    if top_story_variable.get()==1:
        newspaper.write('<h2 align="center">Top Story</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/topstories')
        link_date_time=[date_time,article_link]#creates list containing each articles datetime and link
        database_link_datetime.append(link_date_time)#appends previous list to this list

    if most_read_variable.get()==1:
        newspaper.write('<h2 align="center">Most Read Story</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/mostreadstories')
        link_date_time=[date_time,article_link]
        database_link_datetime.append(link_date_time)

    if politics_headlines_variable.get()==1:
        newspaper.write('<h2 align="center">Politics Headlines</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/politicsheadlines')
        link_date_time=[date_time,article_link]
        database_link_datetime.append(link_date_time)

    if money_headlines_variable.get()==1:
        newspaper.write('<h2 align="center">Money Headline</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/moneyheadlines')
        link_date_time=[date_time,article_link]
        database_link_datetime.append(link_date_time)

    if tech_headlines_variable.get()==1:
        newspaper.write('<h2 align="center">Technology Headline</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/technologyheadlines')
        link_date_time=[date_time,article_link]
        database_link_datetime.append(link_date_time)

    if travel_news_variable.get()==1:
        newspaper.write('<h2 align="center">Travel Headline</h2>\n')
        news_scraper('http://feeds.abcnews.com/abcnews/travelheadlines')
        link_date_time=[date_time,article_link]
        database_link_datetime.append(link_date_time)

    progress_box.insert(INSERT, 'WRITING STORIES TO NEWSPAPER...\n')
    progress_box.update()

    newspaper.write('</body>\n</html>')
    newspaper.close()

    progress_box.insert(INSERT, 'DONE...\n')
    progress_box.configure(state=DISABLED)
    progress_box.update()

    print_button.configure(state=NORMAL)#print button is reactivated so another neswspaper can be printed

print_button=Button(newspaper_generator, text='Print', padx=80 , command=generate_paper, state=DISABLED)
print_button.grid(row=4, column=0, pady=(35,5))

#THIRD SECTION
third_section=Label(newspaper_generator, text='Progess:', font='-weight bold -size 12')
third_section.place(x=10, y=180)

progress_box=Text(newspaper_generator, height=5, width=31, state=DISABLED, bg='black', fg='green')
progress_box.grid(row=6,column=0, pady=(35,5))

#FORTH SECTION
forth_section=Label(newspaper_generator, text='Open Newspaper:', font='-weight bold -size 12')
forth_section.place(x=10, y=305)

def open_file():
    publication_directory=getcwd()+'\publication.html'
    webopen(normpath(publication_directory))

read_button=Button(newspaper_generator, text='Read', padx=80, command=open_file, state=DISABLED)
read_button.grid(row=7,column=0, pady=(40,5))

#FIFTH SECTION
fifth_section=Label(newspaper_generator, text='Save Internet Activity:', font='-weight bold -size 12')
fifth_section.place(x=10, y=380)

def log_activity():
    connection=connect(database='internet_activity.db')
    internet_activity=connection.cursor()
    internet_activity.execute('DELETE FROM Recent_Downloads')
    internet_activity.executemany("INSERT INTO recent_Downloads VALUES(?,?)", database_link_datetime)
    connection.commit()
    internet_activity.close()
    connection.close()

record_button=Button(newspaper_generator, text='Record', padx=80, command=log_activity, state=DISABLED)
record_button.grid(row=8, column=0, pady=(45,5))

newspaper_generator.mainloop()
