from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import event, transaction, finalResult, Profile,PaymentPartner, PaymentRecord, Withdrawal
from datetime import datetime
from django.core.paginator import Paginator
import random

def Home(request):
    if request.user.is_authenticated:

        allEvents = finalResult.objects.all().order_by('-event_id')
        paginator = Paginator(allEvents, 10) # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        transR = transaction.objects.filter(user=request.user).order_by('-id')
        paginator2 = Paginator(transR, 5) # Show 10 contacts per page.
        page_number2 = request.GET.get('page2')
        page_obj2 = paginator2.get_page(page_number2)
      
       

        depositRecord = PaymentRecord.objects.all().order_by('-id')
        withdrawRecord = Withdrawal.objects.all().order_by('-id')
        
        if request.user.id == 1:
            return render(request, "home.html", {
                'events': page_obj, 
                'transactions': page_obj2, 
                'Deposits': depositRecord,
                'Withdrawals': withdrawRecord,
                })
        else:

            return render(request, "home.html", {'events': page_obj, 'transactions': page_obj2})


def ProfileInfo(request):

    return render(request, "profilePage.html")

class SignUpView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"
       
def RechargePage(request):
    if(request.user.is_authenticated):
        Partners = PaymentPartner.objects.all()
        return render(request, "recharge.html", {'paymentPartners': Partners})

def save_withdrawal_request(request):
    if request.user.is_authenticated:   
        if request.method == 'POST':
            # Get the data from the request
            
            amount = request.POST.get('amount')
            payment_method = request.POST.get('payment_method')
            account_number = request.POST.get('account_number')
            account_holder_name = request.POST.get('account_holder_name')
            UPI_id = request.POST.get('UPI_id', None)

            # Create a new withdrawal request
            withdrawal = Withdrawal(user=request.user, 
                                    amount=amount,
                                    payment_method=payment_method, 
                                    account_number=account_number, 
                                    account_holder_name=account_holder_name,
                                    UPI_id=UPI_id)
            withdrawal.save()

            profile_obj = Profile.objects.get(user=request.user)
           
            withAmt = profile_obj.available_Balance - int(amount)
            withAmount = Profile(user=request.user, available_Balance = withAmt)
            withAmount.save()

            # Redirect to a success page or show a success message
            return render(request, 'withdrawalSuccess.html')
        else:
            # Handle the request if the request is not a POST request
            return render(request, "withdrawalPage.html")


    

def SaveUtr(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            amount = request.POST.get('rechargeAmount')
            rchAmt = int(amount)
            upiId = request.POST.get('upiId')
            actualName = request.POST.get('actualName')
            email = request.POST.get('email')
            phoneNumber = request.POST.get('phoneNumber')
            UTRID = request.POST.get('UTRID')

            partner_obj = PaymentPartner.objects.get(upiId=upiId)

            paymentRecord_obj = PaymentRecord(
                user=request.user,
                name=actualName, 
                email=email, 
                phone=phoneNumber, 
                rechargeAmount= rchAmt,
                paymentSentTo = partner_obj,
                UTR_num= UTRID,
                status= "pending"
                )
            paymentRecord_obj.save()
            return JsonResponse({'status':'pyment saved'})

        else:    
            return render(request, "submitUTR.html")

def gameView(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            amount = request.POST.get('Amount')
            amt = int(amount)
            eventId = request.POST.get('LotteryNum')
            colour = request.POST.get('Color')
            luckyNumber = request.POST.get('LuckyNum')
            luckyNumberInt = int(luckyNumber) 
            event_obj = event.objects.get(lotteryNumber=eventId)

            transaction_obj = transaction(user=request.user, amount=amount, colour=colour, luckyNumber=luckyNumberInt, event=event_obj, status="Pending")
            transaction_obj.save()

            profile_obj = Profile.objects.get(user=request.user)
           
            newAmt = profile_obj.available_Balance - amt
            winAmount = Profile(user=request.user, available_Balance = newAmt)
            winAmount.save()

            if luckyNumberInt == -1:

                if colour == 'Red':
                    event_obj.red_count +=amt    
                elif colour == 'Blue':
                    event_obj.blue_count +=amt          
                elif colour== 'Green':
                    event_obj.green_count +=amt

            elif luckyNumberInt >= 0 and luckyNumberInt <= 9:
                if luckyNumberInt == 0:
                    event_obj.zero_count +=amt
                elif luckyNumberInt == 1:
                    event_obj.one_count +=amt
                elif luckyNumberInt == 2:
                    event_obj.two_count +=amt
                elif luckyNumberInt == 3:
                    event_obj.three_count +=amt
                elif luckyNumberInt == 4:
                    event_obj.four_count +=amt
                elif luckyNumberInt == 5:
                    event_obj.five_count +=amt
                elif luckyNumberInt == 6:
                    event_obj.six_count +=amt
                elif luckyNumberInt == 7:
                    event_obj.seven_count +=amt
                elif luckyNumberInt == 8:
                    event_obj.eight_count +=amt
                elif luckyNumberInt == 9:
                    event_obj.nine_count +=amt
            event_obj.save() 

               
            
    return JsonResponse({'status':'Bet created', 'newAmount': newAmt})



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
                nextEvent = event(lotteryNumber = lt+1, start_time = datetime.now(), blue_count= 0, green_count= 0, red_count= 0)
                nextEvent.save()

            winner = event.objects.get(lotteryNumber=lt)   

            try:
                finalResult_obj = finalResult.objects.get(event = winner)
            except finalResult.DoesNotExist:
                if winner:
                    redCount = winner.red_count
                    blueCount = winner.blue_count
                    greenCount = winner.green_count

                    zeroCount = winner.zero_count
                    oneCount = winner.one_count
                    twoCount = winner.two_count
                    threeCount = winner.three_count
                    fourCount = winner.four_count
                    fiveCount = winner.five_count
                    sixCount = winner.six_count
                    sevenCount = winner.seven_count
                    eightCount = winner.eight_count
                    nineCount = winner.nine_count

                    cl = [redCount, greenCount, blueCount]
                    winCol = generateLuckyNumber(cl)
                    if winCol == 0:
                        winColor = "Red"
                    elif winCol == 1:
                        winColor = "Green"
                    elif winCol == 2:
                        winColor = "Blue"


                    

                    Num = [zeroCount, oneCount, twoCount, threeCount, fourCount, fiveCount, sixCount, sevenCount, eightCount, nineCount]
                    winLuckyNum = generateLuckyNumber(Num)

                    finalResult_obj = finalResult(event = winner, colour= winColor, luckyNumber= winLuckyNum)
                    finalResult_obj.save()

                transaction_objs = transaction.objects.filter(event = winner)
                if transaction_objs:
                    for transaction_obj in transaction_objs:
                        if transaction_obj.status == "Pending":

                            if(transaction_obj.colour == winColor or transaction_obj.luckyNumber == Num):
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


def generateLuckyNumber(allnumberCount):
    listNumbers =[]
    minEle = min(allnumberCount)
    for x in range(len(allnumberCount)):
        if allnumberCount[x] == minEle:
            listNumbers.append(x)
            
    randNum = random.randint(0, len(listNumbers) - 1)
    winNum = listNumbers[randNum] 
    return winNum


def confirmRecharge(request):
    if request.user.is_authenticated:
        if request.user.id == 1:

            if request.method == "POST":
                payID = request.POST['paymentID']
                userID = request.POST['userID']
                recAmt = request.POST['recAmt']
                userID=int(userID)
                payID=int(payID)
                recAmt=int(recAmt)
                paymentObj = PaymentRecord.objects.get(id = payID)
                if paymentObj.status == "pending":
                    profile_obj = Profile.objects.get(user_id=userID)
                    recAmt = profile_obj.available_Balance + recAmt
                    recAmount = Profile(user_id=userID, available_Balance = recAmt) 
                    paymentObj.status= "Success"   
                    recAmount.save()
                    paymentObj.save()
                    return JsonResponse({'status':'Recharge Done', 'user': userID, 'amt': recAmt})
                else:
                    return JsonResponse({'status':'Recharge Already Done',})
    

