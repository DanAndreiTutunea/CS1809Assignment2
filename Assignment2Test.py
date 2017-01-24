import sys
from flask import Flask, jsonify, request




class Airport(object):
    def __init__(self, Name, TimeZoneDif):
        self.Name = Name
        self.TimeZoneDif = TimeZoneDif

AirportDB = []

AirportDB.append(Airport("NULL", 0))
AirportDB.append(Airport("LHR", 0))
AirportDB.append(Airport("LGA", 5))
AirportDB.append(Airport("CDG", -1))

Dep_Y = 0
Dep_M = 0
Dep_D = 0
Dep_Hh = 0
Dep_Mm = 0

Arv_Y = 0
Arv_M = 0
Arv_D = 0
Arv_Hh = 0
Arv_Mm = 0

Dep_Air_ID = 0
Arv_Air_ID = 0

Valid_Data = False
Interval = 0
Hours = 0
Minutes = 0
Time_Dil = 0
Exit = False




def Validate_Data():
    Valid_temp = True
    cond_temp = False

    cond_temp = (Dep_Y > 0 and Dep_Y <= 9999 and Dep_M > 0 and Dep_M <= 12 and Dep_D > 0 and Dep_D <= 31 and Dep_Hh >= 0 and Dep_Hh <= 23 and Dep_Mm >= 0 and Dep_Mm < 60)

    if not cond_temp:
        Valid_temp = False
    cond_temp = (Valid_temp and Arv_Y > 0 and Arv_Y <= 9999 and Arv_M > 0 and Arv_M <= 12 and Arv_D > 0 and Arv_D <= 31 and Arv_Hh >= 0 and Arv_Hh <= 23 and Arv_Mm >= 0 and Arv_Mm < 60)

    if not cond_temp:
        Valid_temp = False

    cond_temp = (Valid_temp and Dep_Air_ID > 0 and Dep_Air_ID <= 17678 and Arv_Air_ID > 0 and Arv_Air_ID <= 17678 and (not Dep_Air_ID == Arv_Air_ID))

    if not cond_temp:
        Valid_temp = False

    return Valid_temp


def Calculate_Interval():
    
    Dep_min_temp = (Dep_Y - 1) * 525600 + (Dep_M - 1) * 43200 + (Dep_D - 1) * 1440 + (Dep_Hh - 1) * 60 + Dep_Mm + AirportDB[Dep_Air_ID].TimeZoneDif * 60
    Arv_min_temp = (Arv_Y - 1) * 525600 + (Arv_M - 1) * 43200 + (Arv_D - 1) * 1440 + (Arv_Hh - 1) * 60 + Arv_Mm + AirportDB[Arv_Air_ID].TimeZoneDif * 60
    Interval_temp = Arv_min_temp - Dep_min_temp


    cond_temp = (Arv_M == 2 and Dep_M == 1) or (Arv_M == 4 and Dep_M == 3) or (Arv_M == 6 and Dep_M == 5) or (Arv_M == 9 and Dep_M == 8) or (Arv_M == 11 and Dep_M == 10)
    if cond_temp:
        Interval_temp += 1440

    if (Arv_M == 3 and Dep_D == 29):
        Interval_temp += 1440

    cond_temp = (Arv_Hh >= 2 and Arv_D == 27 and Arv_M == 3) and ((Dep_Hh <= 1 and Dep_D == 27 and Dep_M == 3) or (Dep_D == 26 and Dep_M == 3))
    if cond_temp:
        Interval_temp -= 60

    cond_temp = (Arv_Hh >= 1 and Arv_D == 30 and Arv_M == 10) and ((Dep_Hh <= 2 and Dep_D == 30 and Dep_M == 10) or (Dep_D == 29 and Dep_M == 10))
    if cond_temp:
        Interval_temp += 60

    return Interval_temp







app = Flask(__name__)
@app.route('/')
def index():
    return "Server started"



@app.route('/postData', methods=['POST'])
def postData():

    #nu inteleg de ce e cu print aici
    print request.json

    global Dep_Y
    global Dep_M
    global Dep_D
    global Dep_Hh
    global Dep_Mm

    global Arv_Y
    global Arv_M
    global Arv_D
    global Arv_Hh
    global Arv_Mm

    global Dep_Air_ID
    global Arv_Air_ID

    Dep_Y = request.json['Dep_Y']
    Dep_M = request.json['Dep_M']
    Dep_D = request.json['Dep_D']
    Dep_Hh = request.json['Dep_Hh']
    Dep_Mm = request.json['Dep_Mm']

    Arv_Y = request.json['Arv_Y']
    Arv_M = request.json['Arv_M']
    Arv_D = request.json['Arv_D']
    Arv_Hh = request.json['Arv_Hh']
    Arv_Mm = request.json['Arv_Mm']

    Dep_Air_ID = request.json['Dep_Air_ID']
    Arv_Air_ID = request.json['Arv_Air_ID']

    Valid_Data = Validate_Data()

    if Valid_Data:
        return "Data Valid"
    else:
        return "Data not Valid"

 #   return "got it"


@app.route('/getResult', methods=['GET'])
def getRezult():
    
    global Interval
    global Hours
    global Minutes

    Interval = Calculate_Interval()
    Hours = Interval / 60
    Minutes = Interval % 60
    
    error = "no error"
    if Interval <= 0:
        error = "problem with dates"
    
    return jsonify({'Interval (total minutes)': Interval, 'Hours': Hours, 'Minutes': Minutes, 'error': error})




#nu prea inteleg care e treaba cu asta:
if __name__ == '__main__':
    app.run(debug=True)


