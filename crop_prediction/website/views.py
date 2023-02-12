from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect

# Create your views here.

from .models import users_model
from .serializers import user_serializer
# import main
from .main import main

@csrf_protect
def login(request):
    if (request.method=="POST"):
        email_id = request.POST.get('user_mail_id')
        pwsd = request.POST.get('user_password')
        print(email_id,pwsd)
        if(users_model.objects.filter(email=email_id,password=pwsd)):
            return render(request,'crop_prediction.html',{
                'mailid':email_id,
                })
        return render(request,'login.html',{})
    return render(request,'login.html',{})

def crop_predict(request):
    if(request.method=="POST"):
        email_id = request.POST.get('user_mail_id')
        district = request.POST.get('search_district')
        state = request.POST.get('search_state')
        predict_crop = main(district=district,state=state)
        return render(request,'crop_predicted.html',{
            'mailid':email_id,
            'district':district,
            'state':state,
            "crops":predict_crop,
        })