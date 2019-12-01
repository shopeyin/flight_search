import requests
import datetime
import json
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render,redirect
from flight.forms import FlightForm






payload = {
   "header" : {
   	"cookie" :""
   },
    "body": {
        "email": "customer@travelportal.com",
        "password": "customer"
    }
}

headers = {
        'Host': 'ije-api.tcore.xyz',
        'User-Agent': 'PostmanRuntime/7.18.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referrer': 'http://ije-api.tcore.xyz', 
        'Content-Type':'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
}



def index_view(request): 
    try:
        context ={}
        form = FlightForm()
        if request.method == 'POST':
            form = FlightForm(request.POST)
            if form.is_valid():
                departure_city   = form.cleaned_data.get('departure_city')
                destination_city = form.cleaned_data.get('destination_city')
                departure_date   = form.cleaned_data.get('departure_date')
                return_date      = form.cleaned_data.get('return_date')
                no_of_adult      = form.cleaned_data.get('no_of_adult')
                no_of_child      = form.cleaned_data.get('no_of_child')
                no_of_infant     = form.cleaned_data.get('no_of_adult')
                cabin            = form.cleaned_data.get('cabin')

                
                print(departure_date)
                print(type(departure_date))
                # convert departure date and return date
                new_departure_date = departure_date.strftime("%m/%d/%Y")
               

                new_return_date = return_date.strftime("%m/%d/%Y")
                
                parameters={
                        "header": {
                            "cookie": ""
                        },
                        "body": {
                            "origin_destinations": [
                                {
                                    "departure_city": departure_city  ,
                                    "destination_city": destination_city ,
                                    "departure_date": new_departure_date,
                                    "return_date":  new_return_date, 
                                }
                            ],
                            "search_param": {
                                "no_of_adult": no_of_adult,
                                "no_of_child": no_of_child,
                                "no_of_infant": no_of_infant,
                                "preferred_airline_code" : "",
                                "calendar" :False,
                                "cabin": cabin,
                                
                            }
                        }
                    }
                                

               
                
                new_json = json.dumps(parameters)
                
                urls = 'https://ije-api.tcore.xyz/v1/flight/search-flight'

                result = requests.post(urls,new_json,headers=headers).json()
                
                
                flight ={
                    "departure_date": result['body']['data']['itineraries'][0]['origin_destinations'][0]['segments'][0]['departure']['date'],
                    "departure_time": result['body']['data']['itineraries'][0]['origin_destinations'][0]['segments'][0]['departure']['time'], 
                    "airline":result['body']['data']['itineraries'][0]['origin_destinations'][0]['segments'][0]['operating_airline']['name'],
                    "price":result['body']['data']['itineraries'][0]['pricing']['provider']['total_fare'],
                    "arrival_date":result['body']['data']['itineraries'][0]['origin_destinations'][0]['segments'][0]['arrival']['date'],
                    "arrival_time":result['body']['data']['itineraries'][0]['origin_destinations'][0]['segments'][0]['arrival']['time'],
                }

                context['flight']=flight
                return render(request,"flight/search.html",context=context)
            else:
                context['form']=form
    except ValueError:
        rendered = render_to_string('flight/invalid.html', {'foo': 'bar'})
        response = HttpResponse(rendered)
        return response
    except KeyError:
        rendered = render_to_string('flight/no_flight.html', {'foo': 'bar'})
        response = HttpResponse(rendered)
        return response
   
    return render(request,template_name="flight/home.html",context=context)
    


