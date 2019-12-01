from django import forms

import datetime


# def get_now():
#     return datetime.now().strftime("%m/%d/%Y")

CABIN_CHOICES =( 
    ('First','First'),
    ('Economy','Economy'),
    ('Premium','Premium'),
    ('Business', 'Business'),
    ('All', 'All'),
) 


class DateInput(forms.DateInput):
    input_type='date'
  

class FlightForm(forms.Form):
    departure_city            = forms.CharField(required=True,min_length=3,max_length=3)
    destination_city          = forms.CharField(required=True,min_length=3,max_length=3)
    departure_date            = forms.DateField(widget=DateInput)
    return_date               = forms.DateField(widget=DateInput)
    cabin                     = forms.ChoiceField(choices = CABIN_CHOICES) 
    no_of_adult              = forms.IntegerField()
    no_of_child               = forms.IntegerField()
    no_of_infant            = forms.IntegerField()


    def clean_departure_city(self):
        departure_city = self.cleaned_data.get('departure_city')
        if len(departure_city) != 3:
            raise forms.ValidationError('Input a valid departure name')
        return departure_city

    def clean_no_of_adult(self):
        no_of_adult = self.cleaned_data.get('no_of_adult')
        if no_of_adult < 0 :
            raise forms.ValidationError('number of adult cannot be less than zero')
        return no_of_adult

    def clean_no_of_child(self):
        no_of_child = self.cleaned_data.get('no_of_child')
        if no_of_child < 0:
            raise forms.ValidationError('number of child cannot be less than zero')
        return no_of_child



    def clean_departure_date(self,*args,**kwargs):
        departure_date = self.cleaned_data['departure_date']
        if departure_date < datetime.date.today():
            raise forms.ValidationError("Departure date cannot be less than today's date")
        return departure_date




    def clean(self):
        cleaned_data = super().clean()
        departure_date = self.cleaned_data.get('departure_date')
        return_date =self.cleaned_data.get('return_date')

        if departure_date and return_date:
            if departure_date > return_date:
                raise forms.ValidationError('Depature date is invalid')

        

    
   

    



  
  

       
        