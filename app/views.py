from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from datetime import datetime,timedelta
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, 'app',"models", 'model.pkl')
standscaler_path = os.path.join(BASE_DIR, 'app', 'models', 'standscaler.pkl')
minmaxscaler_path = os.path.join(BASE_DIR, 'app', 'models', 'minmaxscaler.pkl')

# importing model
model = pickle.load(open(model_path,'rb'))
sc = pickle.load(open(standscaler_path,'rb'))
ms = pickle.load(open(minmaxscaler_path,'rb'))
# Create your views here.
def home(r):
    return render(r,'home.html')
@login_required
def dashboard(r):
    return render(r,'dashboard.html')

@login_required
def recommend(request):
    result=""
    crop=""
    if request.method=="POST":
        N = request.POST['Nitrogen']
        P = request.POST['Phosporus']
        K = request.POST['Potassium']
        temp = request.POST['Temperature']
        humidity = request.POST['Humidity']
        ph = request.POST['Ph']
        rainfall = request.POST['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

    return render(request,'recomend.html',{"result":result,"crop":crop})
@login_required
def farm(r,crop):
    if r.method=="POST":
        acres=r.POST["acres"]
        facility=r.POST["facility"]
        investment=r.POST["investment"]
        Production(user=r.user,acres=acres,facility=facility,investment=investment).save()
        return redirect('/productions')
    return render(r,'farm.html')
@login_required
def profile(r):
    return render(r,'account/profile.html')
@login_required
def productions(r):
    data=Production.objects.filter(user=r.user)
    return render(r,'productions.html',{"productions":data})
@login_required
def update_productions(r,id,value):
    data=Production.objects.get(id=id)
    data.production=value
    data.save()
    return redirect('/productions')
@login_required
def rbi(r):
    return render(r,'rbi.html')
@login_required
def crops(r):
    return render(r,'crops.html')
@login_required
def products(r):
    return render(r,'products.html')
@login_required
def buy_products(r,crop):
    data=Product.objects.filter(name=crop)
    return render(r,'buyproducts.html',{"products":data})

@login_required
def sell_products(r,crop):
    if r.method=="POST":
        price=r.POST["price"]
        address=r.POST["address"]
        phone=r.POST["phone"]
        Product(user=r.user,address=address,price=price,phone=phone,name=crop).save()
        return redirect('/myproducts')
    return render(r,'sellproducts.html')
@login_required
def my_products(r):
    data=Product.objects.filter(user=r.user)
    return render(r,'myproducts.html',{"products":data})
@login_required
def edit_products(r,id):
    data=Product.objects.get(id=id)
    if r.method=="POST":
        data.price=r.POST["price"]
        data.address=r.POST["address"]
        data.phone=r.POST["phone"]
        data.save()
        return redirect('/myproducts')
    return render(r,'editproducts.html',{"data":data})
@login_required
def delete_products(r,id):
    data=Product.objects.get(id=id).delete()
    return redirect('/myproducts')
def signout(r):
    logout(r)
    return redirect('/')