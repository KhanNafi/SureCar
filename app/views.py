from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.models import RecommendationFeedback, Recommendations, Wants
from random import randint
from app.models import Car
from django.db.models import Count


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user=request.user
        fname = user.first_name
        return render (request, "home.html", {'fname': fname})
    return render (request, 'home.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        return redirect(signin)
    return render (request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render (request, "home.html", {'fname': fname})
        
        else:
            return redirect(home)

    return render (request, 'signin.html')

def signout(request):
    logout(request)
    return redirect(home)

def browse(request):
    if request.method == "POST":
        minprice = request.POST.get('minimumprice')
        maxprice = request.POST.get('maximumprice')
        filtereddata=Car.objects.filter(price__gte=minprice,price__lte=maxprice).order_by('name')
        return render (request, 'browse.html',{'data':filtereddata})
    data=Car.objects.all().order_by('name')
    return render (request, 'browse.html',{'data':data})

def smartrecommender(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            buyer = request.user
            Recommendations.objects.filter(buyer=buyer).delete()
            year = request.POST.get('year')
            price = request.POST.get('price')
            km_driven = request.POST.get('km_driven')
            mileage = request.POST.get('mileage')
            engine = request.POST.get('engine')
            transmission = request.POST.get('transmission')
            fueltype = request.POST.get('fueltype')
            sellertype = request.POST.get('sellertype')
            owner = request.POST.get('owner')
            seats = request.POST.get('seats')
            user_spec_text = [fueltype,sellertype,transmission,owner,seats]
            cars = Car.objects.all()
            for eachcar in cars.iterator():
                car_text_list = [eachcar.fuel_type, eachcar.seller_type, eachcar.transmission, eachcar.owner, str(eachcar.seats)]
                text_score = len(set(user_spec_text) & set(car_text_list)) / float(len(set(user_spec_text) | set(car_text_list))) * 100
                yearscore = year_score(int(year),int(eachcar.year))
                pricescore = price_score(int(price),int(eachcar.price))
                kmscore = km_score(int(km_driven),int(eachcar.km_driven))
                mileagescore = mileage_score(float(mileage),float(eachcar.mileage))
                enginescore = engine_score(int(engine),int(eachcar.engine))
                numerical_score = ((yearscore)*3 + (pricescore)*4 + kmscore + (mileagescore)*2 + (enginescore)*5)/15
                final_score = (text_score + numerical_score)/2
                carwithscore = Recommendations.objects.create(buyer=buyer,car_id=eachcar.car_id,seller=eachcar.seller,name=eachcar.name,year=eachcar.year,price=eachcar.price,km_driven=eachcar.km_driven,mileage=eachcar.mileage,engine=eachcar.engine,transmission=eachcar.transmission,fuel_type=eachcar.fuel_type,seller_type=eachcar.seller_type,owner=eachcar.owner,seats=eachcar.seats,running_cost=eachcar.running_cost,image=eachcar.image,score=final_score)
                carwithscore.save()
            mostrecommendedcar = Recommendations.objects.filter(buyer=buyer).order_by('-score')[:1]
            for i in mostrecommendedcar.iterator():
                recommendedcarid = i.car_id
            most_recommended_car = Car.objects.get(car_id=recommendedcarid)
            mywants = Wants.objects.create(buyer=buyer,recommended_car_id=most_recommended_car,year=year, price=price, km_driven=km_driven, mileage=mileage, engine=engine, transmission=transmission, fuel_type=fueltype,seller_type=sellertype,owner=owner,seats=seats)
            Wants.objects.filter(buyer=buyer).delete()
            mywants.save()
            return redirect(recommendations)
        return render (request, 'smartrecommender.html')
    return render (request, 'signin.html')

def recommendations(request):
    buyer = request.user
    data=Recommendations.objects.filter(buyer=buyer).order_by('-score')
    return render (request, 'recommendations.html',{'data':data})

def singlerecommendation(request,id):
    car = Car.objects.filter(car_id=id).first()
    buyer=request.user
    userwants = Wants.objects.filter(buyer=buyer).first()
    yeardata = car.year-userwants.year
    pricedata = (userwants.price-car.price)/50000
    kmdrivendata = (userwants.km_driven-car.km_driven)/20000
    mileagedata = float((car.mileage-userwants.mileage)/4)
    enginedata = (userwants.engine-car.engine)/400
    graphdata = [yeardata,pricedata,kmdrivendata,mileagedata,enginedata]
    context = {
        'Car':car,
        'graphdata':graphdata,
    }
    return render (request, 'singlerecommendation.html',context)

def singlerecommendationcontact(request, id):
    car = Car.objects.filter(car_id=id).first()
    myuser = User.objects.filter(username=car.seller).first()
    buyer=request.user
    Wants.objects.filter(buyer=buyer).update(wanted_car_id=car)
    recid = Wants.objects.get(buyer=buyer)
    recommendedcar = Car.objects.get(name=recid.recommended_car_id)
    feedbackid = random_with_defined_digits(10)
    feedbackyear = (percentage_diff (car.year,recommendedcar.year))*100
    feedbackprice = percentage_diff (car.price,recommendedcar.price)
    feedbackkm_driven = percentage_diff (car.km_driven,recommendedcar.km_driven)
    feedbackmileage = percentage_diff (car.mileage,recommendedcar.mileage)
    feedbackengine = percentage_diff (car.engine,recommendedcar.engine)
    feedback = RecommendationFeedback.objects.create(id=feedbackid, year=feedbackyear,price=feedbackprice,km_driven=feedbackkm_driven,mileage=feedbackmileage,engine=feedbackengine)
    feedback.save()
    userwants = Wants.objects.filter(buyer=buyer).first()
    yeardata = car.year-userwants.year
    pricedata = (userwants.price-car.price)/50000
    kmdrivendata = (userwants.km_driven-car.km_driven)/20000
    mileagedata = float((car.mileage-userwants.mileage)/4)
    enginedata = (userwants.engine-car.engine)/400
    graphdata = [yeardata,pricedata,kmdrivendata,mileagedata,enginedata]
    context = {
        'Car':car,
        'Seller':myuser,
        'graphdata':graphdata,
    }
    return render (request, 'singlerecommendationcontact.html', context)

def sell(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = random_with_defined_digits(10)
            seller = request.user
            name = request.POST.get('name')
            year = request.POST.get('year')
            price = request.POST.get('price')
            km_driven = request.POST.get('km_driven')
            mileage = request.POST.get('mileage')
            engine = request.POST.get('engine')
            transmission = request.POST.get('transmission')
            fueltype = request.POST.get('fueltype')
            sellertype = request.POST.get('sellertype')
            owner = request.POST.get('owner')
            seats = request.POST.get('seats')
            running_cost = runningcostclassifier(fueltype,mileage,engine,name)
            image = request.FILES.get('pictureupload')
            mycar = Car.objects.create(car_id=id,seller=seller, name=name, year=year, price=price, km_driven=km_driven, mileage=mileage, engine=engine, transmission=transmission, fuel_type=fueltype,seller_type=sellertype,owner=owner,seats=seats,running_cost=running_cost,image=image,slug=id)
            mycar.save()
        return render (request, 'sell.html')
  
    return render (request, 'signin.html')

def car(request, id):
    car = Car.objects.filter(car_id=id).first()
    context = {
        'Car':car,
    }
    return render (request, 'car.html', context)

def carcontact(request, id):
    car = Car.objects.filter(car_id=id).first()
    myuser = User.objects.filter(username=car.seller).first()
    context = {
        'Car':car,
        'Seller':myuser,
    }
    return render (request, 'carcontact.html', context)

def about(request):
    return render (request, 'about.html')

def analytics(request):
    if request.user.is_superuser:
        recommendations = RecommendationFeedback.objects.all()
        count = 0
        year = 0
        price = 0
        km_driven = 0
        mileage = 0
        engine = 0
        for recommendation in recommendations.iterator():
            count = count + 1
            year = year+recommendation.year
            price = price+recommendation.price
            km_driven = km_driven+recommendation.km_driven
            mileage = mileage+recommendation.mileage
            engine = engine+recommendation.engine
        year = year/count
        price = price/count
        km_driven = km_driven/count
        mileage = mileage/count
        engine = engine/count
        graphdata = [float(year),float(price),float(km_driven),float(mileage),float(engine)]
        totalrecommendationscount = Wants.objects.count()
        distinctrecommendationscount = Wants.objects.all().values('recommended_car_id').distinct().count()
        context = {
            'graphdata':graphdata,
            'distinctrecommendationscount':distinctrecommendationscount,
            'totalrecommendationscount':totalrecommendationscount,
        }
        return render (request, 'analytics.html', context)
    return render (request, 'home.html')

def random_with_defined_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def runningcostclassifier(fueltype,mileage,engine,name):
    if (fueltype=="Diesel"):
        bdtperkm = 80/float(mileage)
    elif (fueltype=="Petrol"):
        bdtperkm = 89/float(mileage)
    elif (fueltype=="LPG"):
        bdtperkm = 54.94/float(mileage)
    elif (fueltype=="CNG"):
        bdtperkm = 47.8/float(mileage)
    
    if (int(engine)<=1500):
        tax = 25000
    elif (int(engine)<=2000):
        tax = 50000
    elif (int(engine)<=2500):
        tax = 75000
    elif (int(engine)<=3500):
        tax = 125000
    elif (int(engine)>=3500):
        tax = 200000

    brand = name.split()[0]

    if (brand=="Volvo" or brand=="Jaguar"):
        yearlymtcost = 300000
    elif (brand=="Mercedes-Benz" or brand=="Audi" or brand=="Volkswagen" or brand=="Land" or brand=="BMW" or brand=="Lexus" or brand=="Chevrolet" or brand=="Ford" or brand=="Jeep" or brand=="Renault" or brand=="Daewoo"  or brand=="Opel"):
        yearlymtcost = 212500
    elif (brand=="Honda" or brand=="Hyundai" or brand=="Kia" or brand=="MG" or brand=="Fiat" or brand=="Skoda" or brand=="Datsun" or brand=="Nissan" or brand=="Mitsubishi"):
        yearlymtcost = 159500
    elif (brand=="Maruti" or brand=="Toyota" or brand=="Mahindra" or brand=="Tata" or brand=="Force" or brand=="Ambassador" or brand=="Ashok" or brand=="Isuzu"):
        yearlymtcost = 125000
    
    finalyearlycost = ((13.1*bdtperkm)*30*12) + tax + yearlymtcost

    if (finalyearlycost<189500):
        classifiedcost = "Very Low"
    elif (finalyearlycost<229500 and finalyearlycost>=189500):
        classifiedcost = "Low"
    elif (finalyearlycost<269500 and finalyearlycost>=229500):
        classifiedcost = "Medium"
    elif (finalyearlycost<309500 and finalyearlycost>=269500):
        classifiedcost = "High"
    elif (finalyearlycost>=309500):
        classifiedcost = "Very High"
    
    return classifiedcost

def year_score (x,y):
    if (x-y==0):
        return 50
    elif (x-y==-1):
        return 66.67
    elif (x-y==-2):
        return 83.34
    elif (x-y<=-3):
        return 100
    elif (x-y==1):
        return 33.33
    elif (x-y==2):
        return 16.66
    elif (x-y==3):
        return 5
    else:
        return 0

def price_score (x,y):
    if (x==y):
        return 50
    elif (y>=0.9*x and y<=x):
        return 66.67
    elif (y>=0.8*x and y<=0.9*x):
        return 83.34
    elif (y>=0.7*x and y<=0.8*x):
        return 100
    elif (y<=1.1*x and y>x):
        return 33.33
    elif (y<=1.2*x and y>1.1*x):
        return 16.66
    elif (y<=1.3*x and y>1.2*x):
        return 5
    else:
        return 0

def km_score (x,y):
    if (((x-y)/1000)>100):
        return 100
    elif (((x-y)/1000)<-100):
        return -100
    else:
        return (x-y)/1000

def mileage_score (x,y):
    if (y>=x-2 and y<=x+2):
        return 100
    elif (y>=x-4 and y<=x+4):
        return 66
    elif (y>=x-8 and y<=x+8):
        return 33
    else:
        return 0

def engine_score (x,y):
    if (y>=x-200 and y<=x+200):
        return 100
    elif (y>=x-500 and y<=x+500):
        return 66
    elif (y>=x-750 and y<=x+750):
        return 33
    else:
        return 0

def percentage_diff (x,y):
    return ((x-y)/y)*100