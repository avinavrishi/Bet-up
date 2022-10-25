from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from accounts.models import Result
from accounts.serializers import ResultSerializer
from rest_framework.decorators import api_view
import json
from .models import event, transaction
from datetime import datetime

class Home(TemplateView):
    template_name = "home.html"


class SignUpView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

    

# @api_view(['GET', 'PUT', 'DELETE'])
# def Result_list(request):
#     if request.method == 'GET':
#         result = Result.objects.all()
#         result_serializer = ResultSerializer(result, many=True)
#         return JsonResponse(result_serializer.data, safe=False)
#     elif request.method == 'PUT':
#         serializer = ResultSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def gameView(request):
    if request.user.is_Authenticated:
        #handle authentication
        if request.method=='POST':
            #In post request send amount, event_id, colour
            postData = json.loads(request.body)
            amount = postData.amount
            colour = postData.colour
            event_obj = postData.event_id
            event_obj = event.object.get(id=event)
            transaction_obj = transaction(user=request.user, amount=amount, colour=colour, event=event_obj)
            transaction_obj.save()
            if colour == 'Red':
                event.red_count+amount
            elif colour == 'Blue':
                event.blue_count+amount
            else:
                event.green_count+amount
            event.save()

            #add return statement return the user to the game

        else:
            #handle get request
            #check if event is running
            last_event = event.objects.latest('id')
            timenow = datetime.now
            if(last_event.end_time>timenow):
                #in case event is running
                #open the current event
                pass
            else:
                newEvent = event()
                #set new event end time
                pass
    else:
        #handle authentication
        pass
            
