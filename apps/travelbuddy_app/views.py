from django.shortcuts import render,redirect,HttpResponse
from models import User,Trip,TravelPlan
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


# Create your views here.
def index(request):
    return render (request,"travelbuddy_app/index.html")
def register(request):
    if request.method == 'POST':
        try:
            validate_email(request.POST['email'])
        except ValidationError as e:
            messages.add_message(request,messages.ERROR, 'Please enter a valid email')
        else:
            password = request.POST['password']
            #hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            user = User.objects.create(name=request.POST['name'],email=request.POST['email'],password=password)
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'Please enter a password of 8 characters or more')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        # unhashed = bcrypt.hashpw(password.encode('utf-8'), hashed)
        user = User.objects.login(email, password)
        if user == False:
            return redirect('/')
        if user == True:
            user_info = User.objects.get(email = email,password = password)
            #storing value in session to use for other features
            request.session['userid'] = user_info.id
            request.session['name'] = user_info.name
            return redirect ('/travels')

def home(request):
    #Getting all user trips
    all_trips = Trip.objects.all()
    your_trips = all_trips.filter(user_id=request.session['userid'])
    user_id = request.session['userid']
    # other_trips = all_trips.exclude(user_id = request.session['userid'])
    other_trips = all_trips.raw('select a.id, a.destination, b.name, a.trip_start_dt, a.description, a.trip_end_dt from travelbuddy_app_trip a JOIN travelbuddy_app_user b on a.user_id = b.id WHERE a.user_id != %s',[user_id])
    other_users = User.objects.exclude(id = request.session['userid'])
    context = {
            'your_trips': your_trips,
            'other_trips': other_trips,
            'other_users': other_users
    }
    print context
    return render (request, 'travelbuddy_app/travels.html', context)

def add(request):
    if request.method == 'POST':

        trip = Trip.objects.create(destination=request.POST['destination'],description=request.POST['description'],trip_start_dt=request.POST['dateFrom'],trip_end_dt=request.POST['dateTo'],user_id = request.session['userid'])
        travel = TravelPlan.objects.create(user_id =request.session['userid'], trip_id =trip.id)
    return render (request, 'travelbuddy_app/add.html')

def get_trip(request,id):
    user = User.objects.all()
    trip = Trip.objects.all()
    trip_id = id
    travelgroup = TravelPlan.objects.raw('select a.id, a.destination, b.name,a.description, a.trip_start_dt, a.trip_end_dt from travelbuddy_app_trip a LEFT JOIN travelbuddy_app_user b on a.user_id = b.id LEFT JOIN travelbuddy_app_travelplan c on c.trip_id = a.id LEFT JOIN travelbuddy_app_travelplan d on d.user_id = b.id WHERE a.id = %s',[trip_id])
    other_travelers = TravelPlan.objects.select_related()
    context = {
        'travelgroup': travelgroup,
        'other_travelers': other_travelers
    }
    return render (request, 'travelbuddy_app/trip.html',context)

def join_trip(request,id):
    Trip_info= Trip.objects.filter(id=id)
    location = Trip_info.values('destination')[0]
    destination = location['destination']
    start = Trip_info.values('trip_start_dt')[0]
    trip_start = start['trip_start_dt']
    end = Trip_info.values('trip_end_dt')[0]
    trip_end = end['trip_end_dt']
    desc = Trip_info.values('description')[0]
    description = desc['description']
    Add_trip = Trip.objects.create(destination=destination,description = description,trip_start_dt = trip_start,trip_end_dt = trip_end,user_id = request.session['userid'])
    join_trip = TravelPlan.objects.create(user_id =request.session['userid'], trip_id =id)
    return redirect ('/travels')


def logout(request):
    request.session['userid'] = 0
    return redirect ('/')
