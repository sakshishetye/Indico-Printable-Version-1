
from flask import Flask, render_template,jsonify, request,send_file, current_app as app
import urllib.request as urllib2
import ssl, json
import datetime
from datetime import date
import pdfkit
import psycopg2
import psycopg2.extras
import mysql
import pymysql
from app import app
from db_config import mysql
from flaskext.mysql import MySQL

app = Flask(__name__)

@app.route('/')
def home (): 
     return render_template('calendar_event.html')

@app.route('/calendar-events')
def calendar_events():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT event_id, title, category, speaker, room, date, time, podcast,url as end FROM event")
        rows = cursor.fetchall()
        resp = jsonify({'success' : 1, 'result' : rows})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()         

@app.route('/template', methods=['GET', 'POST'])
def choose_template():
    conn = pymysql.connect(
    host ='localhost',
    user ="root",
    passwd ="Sakshi@02",
    database="calender",
    cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM event")
    #cursor.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event")
    results = cur.fetchall()
    if request.method=='POST':
        title = request.form['title']
        url = request.form['url']
        print[url]
        date = request.form['date']
        time = request.form['time']
        #class1 = request.form['class']
        id = request.form['id']
        event = event(title=title, url=url, date=date, time=time, id=id)
        cur.execute
        conn.commit() 
        cur.close()
        msg = 'success'

    return render_template('choose_template.html', calender=results)

@app.route('/print_template', methods=['GET', 'POST'])
def print_template():
    if request.method=='POST':
        
        temp = request.form.get('notice')
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        oneweek = datetime.timedelta(days=6)
        week = today + oneweek
        day = datetime.date.today().weekday()
        firstday = today
        lastday = week        

        f_search = firstday.strftime("%Y-%m-%d")
        t_search = lastday.strftime("%Y-%m-%d")

        url = "https://indico.cern.ch/export/categ/0.json?f=2022-07-01&t=2022-07-01&order=start" + f_search + "&t=" + t_search + "&order=start"
        print(url)
        NOTrequest = urllib2.Request(url)
        response = urllib2.urlopen(NOTrequest, context=ssl._create_unverified_context())
        data = json.loads(response.read())
        n=data['count']


        if temp=='daa':
            body = """
            <!-- daa.html -->

            <body>
                <html>

                <head>
                    <title>TIFR</title>
                    <style>
                        body {
                            height: 1000px;
                            width: 850px;
                            margin-left: auto;
                            margin-right: auto;
                        }
                    </style>

                </head>


                <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">
                    <center>
                        <h2>TATA INSTITUTE OF FUNDAMENTAL RESEARCH</h2>
                        <h1><b>
                                <font color="blue"><i>Department of Astronomy & Astrophysics</i></font>
                            </b></h1>
                            

                    </center>
                    <center>
                        <h1> Seminar</h1>
                    </center>
                    <hr>
                    <P style="margin-left: 20px;">
                    <table>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Title </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_TITLE </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> url </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_URL </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Start Date & Time </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> End Date & Time </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Location </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_LOCATION </h3>
                            </td>
                        </tr>
                    </table>
                    </p>

                    <h3>
                        <center> <u> Abstract: </u> </center>
                    </h3>
                    <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>

                    <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
                </body>

                </html>
            """
        elif temp=='dbs':
            body = """
                <html>
                    <head>
                        <title> DBS Notice Layout </title>
                        <style>
                            body {
                                height: 1000px;
                                width: 850px;
                                margin-left: auto;
                                margin-right: auto;
                            }
                            </style>
                    </head>

                    <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">

                        <h1> Seminar DEPARTMENT OF BIOLOGICAL SCIENCES </h1>
                        <h3 style="text-align: center;"> Tata Institute Of Fundamental Research, Homi Bhabha Road, Mumbai-400 005 </h3>
                        <hr>
                                
                        <P style="margin-left: 50px;">
                        <table>
                                <tr>
                                    <td style="width: 200px;">
                                        <h3> Title </h3>
                                    </td>
                                    <td style="width: 40px; text-align: center;">
                                        <h3> : </h3>
                                    </td>
                                    <td>
                                        <h3> MAIN_TITLE </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width: 200px;">
                                        <h3> url </h3>
                                    </td>
                                    <td style="width: 40px; text-align: center;">
                                        <h3> : </h3>
                                    </td>
                                    <td>
                                        <h3> MAIN_URL </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width: 200px;">
                                        <h3> Start Date & Time </h3>
                                    </td>
                                    <td style="width: 40px; text-align: center;">
                                        <h3> : </h3>
                                    </td>
                                    <td>
                                        <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width: 200px;">
                                        <h3> End Date & Time </h3>
                                    </td>
                                    <td style="width: 40px; text-align: center;">
                                        <h3> : </h3>
                                    </td>
                                    <td>
                                        <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width: 200px;">
                                        <h3> Location </h3>
                                    </td>
                                    <td style="width: 40px; text-align: center;">
                                        <h3> : </h3>
                                    </td>
                                    <td>
                                        <h3> MAIN_LOCATION </h3>
                                    </td>
                                </tr>
                            </table>
                        </p>

                        <p> (ALL ARE WELCOME) </p>

                        <h3>
                                <u> Abstract: </u> 
                            </h3>
                            <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>

                            <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
                    </body>
                </html>    
                """
        elif temp=='dcmp': 
            body = """
        <html>
            <head>
                <title>TIFR</title>
                <style>
                <body> {
                    height: 1000px;
                    width: 850px;
                    }
                    </style>
            </head>
            <body topmargin="30px" bottommargin="30px" leftmargin="50px" rightmargin="50px">
            <h1 style="text-align: center;">TATA INSTITUTE OF FUNDAMENTAL RESEARCH</h1>
            <h2 style="text-align: center;">CONDENSED MATTER PHYSICS AND MATERIALS</h2>
            <h1 style="text-align:center;">Science Seminar</h1>
            <p style="margin-left: 20px;">
                <table>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Title </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_TITLE </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> url </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_URL </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Start Date & Time </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> End Date & Time </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;">
                                <h3> Location </h3>
                            </td>
                            <td style="width: 40px; text-align: center;">
                                <h3> : </h3>
                            </td>
                            <td>
                                <h3> MAIN_LOCATION </h3>
                            </td>
                        </tr>
                    </table>
                </p>

                    <h3>
                        <u> Abstract: </u> 
                    </h3>
                    <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>

                    <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
            </td>
        </body>
        </html>    
        """       
        elif temp=='dcs':
            body = """
                <html>
                    <head>
                        <title> tifr</title>
                        <style>
                        h2{
                            background-color:grey;
                            color:black;

                        }
                            body {
                                height: 1000px;
                                width: 850px;
                                margin-left: auto;
                                margin-right: auto;
                                }
                            </style>
                    </head>

                    <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">
                <center> <h1><b><u>TATA INSTITUTE OF FUNDAMENTAL RESEARCH</b></u></h1> </center>
                <center><h2><big>Chemical Sciences Seminar</big></h2></center>
                
                        <P style="margin-left: 20px;">
                        <table>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Title </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_TITLE </h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> url </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td>  
                                    <h3> MAIN_URL </h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Start Date & Time </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> End Date & Time </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Location </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_LOCATION </h3>
                                </td>
                            </tr>
                        </table>
                        </p>

                        <h3> <u> Abstract: </u> </h3>
                        <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>
                        
                        <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
                    </body>
                </html>    
                """

        elif temp=='dhep':
            body = """
                <html>
                    <head>
                        <title> DHEP Notice Layout </title>
                        <style>
                            body {
                                height: 1000px;
                                width: 850px;
                                margin-left: auto;
                                margin-right: auto;
                            }
                            </style>
                    </head>

                    <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">

                        <h1 style="text-align: center;"> TATA INSTITUTE OF FUNDAMENTAL RESEARCH </h1>
                        
                        <h2 style="text-align: center; margin-top: 50px"> High Energy Physics Seminar </h2>
                        
                                <P style="margin-left: 20px;">
                        <table>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Title </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_TITLE </h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> url </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td>  
                                    <h3> MAIN_URL </h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Start Date & Time </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> End Date & Time </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Location </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_LOCATION </h3>
                                </td>
                            </tr>
                        </table>
                        </p>

                        <h3> <u> Abstract: </u> </h3>
                        <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>
                        
                        <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
                    </body>
                </html>     
                """
        elif temp=='dnap':
            body = """
                <html>
                    <head>
                        <title> DNAP </title>
                        <style>
                            body {
                                height: 1000px;
                                width: 850px;
                                margin-left: auto;
                                margin-right: auto;
                            }
                            </style>
                    </head>

                    <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">

                        <h1 style="text-align: center;"> TATA INSTITUTE OF FUNDAMENTAL RESEARCH </h1>
                        <h2 style="text-align: center;"> <FONT COLOR="RED">Department of Nuclear Atomic Physics</FONT> </h2>
                        <h1 style="text-align: center;"><FONT COLOR="BLUE"> SEMINAR</FONT> </h1>
                        
                        <P style="margin-left: 20px;">
                        <table>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Speaker</h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_SPEAKER </h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3>Title</h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td>  
                                    <h3> MAIN_TITLE</h3> 
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3>  Date </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_DATE </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Time </h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;"> 
                                    <h3> Venue</h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3> : </h3> 
                                </td>
                                <td> 
                                    <h3> MAIN_VENUE </h3>
                                </td>
                            </tr>
                        </table>
                        </p>

                        <h2 > <I>Abstract</I> </h2>
                        <p style="text-align: justify"> MAIN_DESCRIPTION </p>
                        
                        <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br>  DNAP Office</h3>
                    </body>
                </html>   
                """

        
        elif temp=='dtp':
            body = """
                <html>
                    <head>
                        <title>TIFR</title>
                        <style>
                        body {
                                height: 1000px;
                                width: 850px;
                                margin-left: auto;
                                margin-right: auto;
                                }
                            </style>
                    </head>
                    <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">
                    <h1 style="text-align: center;"style="text-align: center;">TATA INSTITUTE OF FUNDAMENTAL RESEARCH</h1>
                    <b><h3 style="text-align: center;">Homi Bhaba Road,Mumbai-400 005</h3></b>
                    <h3 style="text-align:right;"><b>June 9,2022</b></h3>
                    <h2 style="text-align: center;"><p style="background-color:blue;color:white">Department Of Theoretical Physics</p></h2>
                    <h3 style="text-align: center;"><p style="color:red;">ASET Colloquium</p></h3>
                    <p style="margin-left: 20px;">

                    <table> 
                            <tr>
                                <td style="width: 100px;",colspan="2"> 
                                <h3 style="color:blue;">Title</h3>
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3 style="color:blue;">:</h3> 
                                </td>
                                <td> 
                                    <h3><p style="color:blue;">MAIN_TITLE</p> </i> </h3> </td>
                            </tr>
                            <tr>
                                <td style="width: 60px;",colspan="2"> 
                                    <h3 ><p style="color:blue;">Link</p></h3> 
                                </td>
                                <td style="width: 20px; text-align: center;"> 
                                    <h3><p style="color:blue;">:</p></h3> 
                                </td>
                                <td> 
                                    <h3><p style="color:blue;">MAIN_ADDRESS</p></h3>
                                </td>
                            </tr>
                        
                            <tr>
                                <td style="width: 100px;",colspan="2"> 
                                    <h3><p style="color:blue;">Start Date</p></h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3><p style="color:blue;">:</p></h3> 
                                </td>
                                <td> 
                                    <h3><p style="color:blue;">MAIN_START_DATE<p style="color:blue;"></h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 100px;",colspan="2"> 
                                    <h3><p style="color:blue;">End Date</p></h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3><p style="color:blue;">:</p> </h3> 
                                </td>
                                <td> 
                                    <h3><p style="color:blue;">MAIN_END_DATE</p></h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 100px;",colspan="2"> 
                                    <h3><p style="color:blue;">Location</p></h3> 
                                </td>
                                <td style="width: 40px; text-align: center;"> 
                                    <h3><p style="color:blue;">:</p></h3> 
                                </td>
                                <td> 
                                    <h3><p style="color:blue;">MAIN_LOCATION</p></h3>
                                </td>
                            </tr>
                        </table>
                        </p>

                            <tr>
                                <td >   
                                </td>
                                <td >
                                </td>
                                <td> 
                                <h2 style="text-align:left;"><p style="color:brown;"><i>Abstract</i></p></h2> 
                                <h3><p style="color:brown;">MAIN_DESCRIPTION</p></h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width:60px;"> 
                                    <h3 style="color:red;"> </h3> 
                                </td>
                                <td> 
                                    <h3 style="color:brown;"> </h3>
                                </td>
                                <td> 
                                    <h3 style="text-align:right"><p style="color:brown;">Organizer</p></h3> 
                                    <h3 style="text-align:right"><p style="color:brown;">MAIN_ORGANIZER</p></h3>
                                </td>
                            </tr>
                    </body>
                </html>    
                """
        elif temp=='wednesday':
             body = """
            <html>
                <head>
                    <title> Wednessday Colloquium Notice Layout </title>
                    <style>
                        body {
                            height: 1000px;
                            width: 850px;
                            margin-left: auto;
                            margin-right: auto;
                        }
                        </style>
                </head>

                <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">

                    <h1 style="text-align: center;"> TATA INSTITUTE OF FUNDAMENTAL RESEARCH </h1>
                    <h3 style="text-align: center;"> Homi Bhabha Road, Mumbai-400 005 </h3>
                    <h4 style="text-align: right; margin-right: 40px;"> MAIN_CREATION_DATE_DATE <br> (at MAIN_CREATION_DATE_TIME) </h4>
                    <h1 style="text-align: center;"> <font size="px" color="#00008B"> <b> WEDNESSDAY COLLOQUIUM </b> </font> </h1>
                    
                    <P style="margin-left: 20px;">
                    <table>
                        <tr>
                            <td style="width: 200px;"> 
                                <h3> Title </h3> 
                            </td>
                            <td style="width: 40px; text-align: center;"> 
                                <h3> : </h3> 
                            </td>
                            <td> 
                                <h3> MAIN_TITLE </h3> 
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;"> 
                                <h3> url </h3> 
                            </td>
                            <td style="width: 40px; text-align: center;"> 
                                <h3> : </h3> 
                            </td>
                            <td>  
                                <h3> MAIN_URL </h3> 
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;"> 
                                <h3> Start Date & Time </h3> 
                            </td>
                            <td style="width: 40px; text-align: center;"> 
                                <h3> : </h3> 
                            </td>
                            <td> 
                                <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;"> 
                                <h3> End Date & Time </h3> 
                            </td>
                            <td style="width: 40px; text-align: center;"> 
                                <h3> : </h3> 
                            </td>
                            <td> 
                                <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 200px;"> 
                                <h3> Location </h3> 
                            </td>
                            <td style="width: 40px; text-align: center;"> 
                                <h3> : </h3> 
                            </td>
                            <td> 
                                <h3> MAIN_LOCATION </h3>
                            </td>
                        </tr>
                    </table>
                    </p>

                    <h3> <u> Abstract: </u> </h3>
                    <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>
                    
                    <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>

                </body>
            </html>  
            """

        else:
             body = """
            <html>
                <head>
                    <title> ASET Colloquium Notice Layout </title>
                    <style>
                        body {
                            height: 1000px;
                            width: 850px;
                            margin-left: auto;
                            margin-right: auto;
                        }
                        </style>
                </head>

                <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">

                    <h1 style="text-align: center;"> TATA INSTITUTE OF FUNDAMENTAL RESEARCH </h1>
                    <h3 style="text-align: center;"> Homi Bhabha Road, Mumbai-400 005 </h3>
                    
                    <hr>
                    <h3 style="text-align: center;"> ASET Colloquium </h3>
                    
                    <P style="margin-left: 20px;">
                    <table>
                            <tr>
                                <td style="width: 200px;">
                                    <h3> Title </h3>
                                </td>
                                <td style="width: 40px; text-align: center;">
                                    <h3> : </h3>
                                </td>
                                <td>
                                    <h3> MAIN_TITLE </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;">
                                    <h3> url </h3>
                                </td>
                                <td style="width: 40px; text-align: center;">
                                    <h3> : </h3>
                                </td>
                                <td>
                                    <h3> MAIN_URL </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;">
                                    <h3> Start Date & Time </h3>
                                </td>
                                <td style="width: 40px; text-align: center;">
                                    <h3> : </h3>
                                </td>
                                <td>
                                    <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;">
                                    <h3> End Date & Time </h3>
                                </td>
                                <td style="width: 40px; text-align: center;">
                                    <h3> : </h3>
                                </td>
                                <td>
                                    <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                                </td>
                            </tr>
                            <tr>
                                <td style="width: 200px;">
                                    <h3> Location </h3>
                                </td>
                                <td style="width: 40px; text-align: center;">
                                    <h3> : </h3>
                                </td>
                                <td>
                                    <h3> MAIN_LOCATION </h3>
                                </td>
                            </tr>
                        </table>
                    </p>

                            <u> Abstract: </u> 
                        </h3>
                        <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>

                        <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
                </body>
            </html>    
            """


        body=body.replace('MAIN_TITLE',data['results'][0]['title'])
        body=body.replace('MAIN_DESCRIPTION',data['results'][4]['description'])
        body=body.replace('MAIN_START_DATE',data['results'][0]['startDate']['date'])
        body=body.replace('MAIN_END_DATE',data['results'][0]['endDate']['date'])
        body=body.replace('MAIN_LOCATION',data['results'][0]['location'])
        body=body.replace('MAIN_ADDRESS',data['results'][0]['address'])
        body=body.replace('MAIN_ORGANIZER',data['results'][0]['organizer'])
        body=body.replace('MAIN_URL',data['results'][0]['url'])

        pdfkit.from_string(body, 'notice.pdf')

        path = "/codes/dropdown/cevents/notice.pdf"
        return send_file(path, as_attachment=True)
        

@app.route('/createdb', methods=['GET', 'POST'])
def createdb():
    conn = None
    cursor = None
    if request.method=='POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            f_search = request.form.get('S_Date')
            t_search = request.form.get('T_Date')

            url = "https://indico.cern.ch/export/categ/0.json?f=2022-07-01&t=2022-07-01&order=start" + f_search + "&t=" + t_search + "&order=start"
            print(url)
            NOTrequest = urllib2.Request(url)
            response = urllib2.urlopen(NOTrequest, context=ssl._create_unverified_context())
            datalist = json.loads(response.read())
             # Reading from file
            # datalist = json.loads(f.read())
            print(len(datalist['results']))      

            for res in datalist['results']:
                    # print(" ",res['title']) 
           
                body="INSERT INTO event values ('MAIN_ID','MAIN_TITLE','MAIN_CATEGORY','MAIN_SPEAKER','MAIN_ROOM','MAIN_DATE','MAIN_TIME','MAIN_PODCAST','MAIN_URL')"

                body=body.replace('MAIN_ID',res['id'])
                body=body.replace('MAIN_TITLE',res['title'])
                body=body.replace('MAIN_CATEGORY',res['category'])
                body=body.replace('MAIN_SPEAKER',res['creator']['fullName'])
                body=body.replace('MAIN_ROOM',res['room'])
                body=body.replace('MAIN_DATE',res['startDate']['date'])
                body=body.replace('MAIN_TIME',res['startDate']['time'])
                body=body.replace('MAIN_PODCAST',res['address'])
                body=body.replace('MAIN_URL',res['url'])
                
                print(body)
                cursor.execute(body)

                conn.commit()                        
        except Exception as error: 
                print(error)

        finally:

                if cursor is not None:
                        cursor.close
                if conn is not None:
                        conn.close 

    return('Events imported successfully')                            
            
@app.route('/create_date')
def create_date():
    return render_template('create_date.html')

@app.route('/search')
def search():
    return render_template('search_date.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') ,404

if __name__ == '__main__':
    app.debug = True
    app.run()