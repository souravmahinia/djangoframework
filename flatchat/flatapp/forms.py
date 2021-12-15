from django import forms
from flatapp.models import add_prperty

class add_property_form(forms.ModelForm):
    class Meta:
        model = add_prperty
        exclude = ["seller"]

                


'''

 fields = ["property_name","property_price","booking_amount","property_image1",
                  "property_image2","property_image3","property_image4",
                  "property_type","property_status","area","no_of_bedrooms","no_of_bathrooms",
                  "is_Air_Conditioning","is_Gym","is_Laundry_room","is_TV_Cable","is_Wifi",
                  "is_Parking","is_Swimming_Pool","description"]
'''
                  