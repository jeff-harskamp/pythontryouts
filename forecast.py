
import requests
from tkinter import *

'''
This is my first attempt at making a small app.
Also first time making something in Python.

The purpose of the app is to find the ideal moment to make use of your solar panels.
My assumption is that it is best to immediately use energy,
instead of converting it back and forth to send back it to the grid.

You input the amount of hours you expect to using the energy, 
enter your latitude and longitude (use google maps),
and lastly enter your weatherapi.com API key (not gonna share my own here of course, it's free so you can create your own key).

This is a work in progress so i can learn using Python.
planning on adding functionality of amount of energy used and created.

Feedback is welcome.
'''


#initialize arrays
dayA=[]
timeA=[]
cloudA=[]
isdayA=[]

# method to get data fromweatherapi.com and feed into data processor 
def getForecast(url):
    res = requests.get(url, stream=True)
    res_dict = res.json()
    retrieveHourlyData(res_dict)

# Iterates over json response to fill arrays with data
def retrieveHourlyData(json):
    i = 0
    # one i per day
    while i < 3:
        j = 0
        # one j per hour
        while j < 24:
            isdayA.append(json['forecast']['forecastday'][i]['hour'][j]['is_day'])
            timestamp = json['forecast']['forecastday'][i]['hour'][j]['time']
            tsA = timestamp.split()
            dayA.append(tsA[0])
            timeA.append(tsA[1])
            cloudA.append(100-(json['forecast']['forecastday'][i]['hour'][j]['cloud']))
            j += 1
        i += 1

def getBestPeriod(hours,lat,lon,key):
    # Build request using parameters
    req = f'http://api.weatherapi.com/v1/forecast.json?key={key}&q={lat},{lon}&days=7'
    getForecast(req)
    # initialize data
    i = 0
    p = hours
    Sum = 0
    Best = 0
    Bestp = 0
    # Calculate best period
    while p < len(cloudA):
        # only calculate if in the same day 
        if dayA[i] == dayA[p] and p < len(cloudA) and isdayA[i] == 1 and isdayA[p] == 1 :
            Sum = sum(cloudA[i:p])
            # check if sum is better than the best, take index and sum if true
            if Sum > Best:
                Bestp = i
                Best = Sum
        i +=1
        p +=1
    
    BestDay = str(dayA[Bestp])
    BestTime = str(timeA[Bestp])
    Average = str(Best / hours)

    return("You will get the best result when you start on " + BestDay + ", at " + BestTime + ".\nYou will get an average of " + Average + "% sun then. " )



'''
Here is an attempt at creating a simple.
It's something...
'''
window = Tk()
window.geometry('850x400')
window.title("Best period of sunshine")

hour = Label(window, text="How many hours of sun do you need?", font=("Arial Bold", 14))
hour.grid(column=0, row=0)

hours = Entry(window,width=10)
hours.grid(column=0, row=1)

geo = Label(window, text="On what position do you need the data? Use Latitude and Longitude", font=("Arial Bold", 14))
geo.grid(column=0, row=3)

ltl = Label(window, text="Latitude", font=("Arial Bold", 14))
ltl.grid(column=0, row=4)

lati = Entry(window,width=10)
lati.grid(column=1, row=4)

lol = Label(window, text="Longitude", font=("Arial Bold", 14))
lol.grid(column=0, row=5)

long = Entry(window,width=10)
long.grid(column=1, row=5)

apikey = Label(window, text="please fill in your weatherapi.com API key", font=("Arial Bold", 14))
apikey.grid(column=0, row=6)

key = Entry(window,width=100)
key.grid(column=0, row=7)

response = Label(window, text="", font=("Arial Bold", 15))
response.grid(column=0, row=10)

def clicked():
    result = getBestPeriod(int(hours.get()),(lati.get()),(long.get()),(key.get()))
    response.configure(text= result)

btn = Button(window, text="Find", command=clicked)
btn.grid(column=0, row=9)
window.mainloop()
