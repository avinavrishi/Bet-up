from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import event, transaction, finalResult, Profile,PaymentPartner
from datetime import datetime

def Home(request):
    allEvents = finalResult.objects.all().order_by('-event_id')
    transR = transaction.objects.filter(user=request.user)
    return render(request, "home.html", {'events': allEvents, 'transactions': transR})

class SignUpView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"
       
def RechargePage(request):
    Partners = PaymentPartner.objects.all()
    return render(request, "recharge.html", {'paymentPartners': Partners})

def gameView(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            amount = request.POST.get('Amount')
            amt = int(amount)
            eventId = request.POST.get('LotteryNum')
            colour = request.POST.get('Color')

            event_obj = event.objects.get(lotteryNumber=eventId)

            transaction_obj = transaction(user=request.user, amount=amount, colour=colour, event=event_obj, status="Pending")
            transaction_obj.save()
            profile_obj = Profile.objects.get(user=request.user)

            newAmt = profile_obj.available_Balance - amt
            winAmount = Profile(user=request.user, available_Balance = newAmt)
            winAmount.save()


            if colour == 'Red':
                event_obj.red_count +=amt    

            elif colour == 'Blue':
                event_obj.blue_count +=amt          
            else:
                event_obj.green_count +=amt
            event_obj.save()    
            
    return JsonResponse({'status':'Bet created', 'newAmount': newAmt })


def finalResults(request):
    if request.method == "POST":
        
        lotNum = request.POST['lotnum']
        winColor = ""
        lt = int(lotNum)
        if request.user.id == 1:
            #CREATING NEW BLANK EVENT BEFORE FINDING THE RESULT
            try:
                nextEvent = event.objects.get(lotteryNumber=lt+1)
            except event.DoesNotExist:
                nextEvent = event(lotteryNumber = lt+1, blue_count= 0, green_count= 0, red_count= 0)
                nextEvent.save()

            winner = event.objects.get(lotteryNumber=lt)   

            try:
                finalResult_obj = finalResult.objects.get(event = winner)
            except finalResult.DoesNotExist:
                if winner:
                    redCount = winner.red_count
                    blueCount = winner.blue_count
                    greenCount = winner.green_count
                    
                    if(redCount < blueCount and redCount < greenCount):
                        print("red")
                        winColor = "Red"
                    elif(blueCount < greenCount and blueCount < redCount):
                        print("blue")
                        winColor = "Blue"
                    else:
                        print("Green")
                        winColor = "Green"
                    finalResult_obj = finalResult(event = winner, colour= winColor)
                    finalResult_obj.save()

                transaction_objs = transaction.objects.filter(event = winner)
                if transaction_objs:
                    for transaction_obj in transaction_objs:
                        if transaction_obj.status == "Pending":

                            if(transaction_obj.colour == winColor):
                                transaction_obj.status="Success"
                                transaction_obj.save()
                                profile_obj = Profile.objects.get(user=transaction_obj.user)
                                newAmt = profile_obj.available_Balance + (transaction_obj.amount*2)
                                winAmount = Profile(user=transaction_obj.user, available_Balance = newAmt)    
                                winAmount.save()
                            else:
                                transaction_obj.status="Failed"
                                transaction_obj.save()
                        else:
                            pass
            else:
                pass

            

        
    return JsonResponse({'status':'Result printed'})