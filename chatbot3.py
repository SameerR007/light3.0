from flask import Flask,request,jsonify
import requests
from geopy.geocoders import Nominatim
from datetime import date
app= Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    try:
        data=request.get_json()
        score=data['queryResult']['parameters']['score']
        print(score)
        if score=="score":
            url="https://api.cricapi.com/v1/currentMatches?apikey=71b6bf09-6ca5-4259-9c69-95288ea0eec9&offset=0"
            response=requests.get(url)
            response=response.json()
            name1=response['data'][0]['name']
            status1=response['data'][0]['status']
            venue1=response['data'][0]['venue']
            name2=response['data'][1]['name']
            status2=response['data'][1]['status']
            venue2=response['data'][1]['venue']
            final1="The match {} played at {} has the following status - {}.".format(name1,venue1,status1)
            final2="In the another match {} played at {} has the following status - {}.".format(name2,venue2,status2)   
            final=final1+'\n'+final2   
            print(final)
        ft={"fulfillment_text":final}
        return jsonify(ft)
    except:
        today = date.today()
        
        source_city=data['queryResult']['parameters']['geo-city']
        
        datee=data['queryResult']['parameters']['date']
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(source_city)
        lat=location.latitude
        lon=location.longitude

        if datee!="" and (int(datee[8:10]) != (int(str(today)[8:10]))) :
            url="https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=013b716d17cad1e8064a6a092a8cf06d".format(lat,lon)
            response=requests.get(url)
            response=response.json()
            weather=response['list'][7]['weather'][0]['main']
            description=response['list'][7]['weather'][0]['description']
            min_temp=round(float(response['list'][7]['main']['temp_min']-273.15),2)
            max_temp=round(float(response['list'][7]['main']['temp_max']-273.15),2)
            final="Tomorrow's weather in {} is mainly {},more specifically {}. Minimum temperature will be around {}C while maximum temperature being around {}C.".format(source_city,weather,description,min_temp,max_temp)   
            ft={"fulfillmentText":final}
            return jsonify(ft)
        else :
            url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=013b716d17cad1e8064a6a092a8cf06d".format(lat,lon)
            response=requests.get(url)
            response=response.json()
            current_temp=round(float(response['main']['temp']-273.15),2)
            min_temp=round(float(response['main']['temp_min']-273.15),2)
            max_temp=round(float(response['main']['temp_max']-273.15),2)
            weather=response['weather'][0]['main']
            description=response['weather'][0]['description']
            final="Today the weather in {} is mainly {},more specifically {}. Current temprature is approximately {}C with minimum temperature {}C and maximum temperature {}C.".format(source_city,weather,description,current_temp,min_temp,max_temp)
            ft={"fulfillmentText":final}
            return jsonify(ft)        

if __name__=="__main__":

    app.run()