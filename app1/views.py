import json
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from git import Object

from app1.forms import SignUpForm
from .models import PointVect, vect
from django.views.generic.base import View, TemplateView
from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.serializers import serialize
from .models import vect
from django.contrib.gis.geos import Point

# Create your views here.


class IndexView(TemplateView):
    # a template file name in the templates directory in current application
    template_name = 'ol-index.html'

    def get_context_data(self, **kwargs):
        return kwargs

class BoundariesGeoJSON(View):
    def get(self, request):
        qs=list(PointVect.objects.values('gid','name','geom'))
        geojson = {}
        for geom in qs:
            geometry = geom['geom']
            
            geojson = serialize('geojson', PointVect.objects.filter(geom__contains=geometry),
            geometry_field='geom',
            fields=('amp_namt',))
            print(geometry[0])
            print('/n')
            
        return HttpResponse(geojson)

def mapview(request):
    
    qs=list(PointVect.objects.values('gid','name','geom'))
    
    geojson = []
    
    for geom in qs[:1]:
        geometry = geom['geom']
        x = geometry[0]
        y = geometry[1]
        latlon = {
            'lat':y,
            'lon':x
        }
        geojson.append(latlon)
        
    print(geojson)
    showVector = 'false'
    if(request.user.is_staff):
        showVector = 'true'
            
    print(request.user.is_staff)
    mapData = {'showVector': showVector ,'geom':json.dumps(geojson)}
    return render(request,"index.html",{'vect': mapData})

def user_login(request):
    if request.method == "POST":
        userinfo = User.objects.get(username=request.POST['username'])
        username = userinfo.username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            alert = True
            return render(request, "login.html", {'alert':alert})
        
    return render(request, "login.html")

#Register admin
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        try: 
            if not User.objects.get(username=request.POST['username']):
                return HttpResponse('This username id already registered')
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                print(user)
                return redirect('login')
        except:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                print(user)
                return redirect('login')
            
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#code for logout
def Logout(request):
    logout(request)
    return redirect ("/login")