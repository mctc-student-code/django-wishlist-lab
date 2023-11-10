from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required#ensuring views are only visible while logged in
from django.http import HttpResponseForbidden #security library? 

"""Views are the controller, sending specific responses to be displayed"""
@login_required
def place_list(request):#function takes only request argument. Will be called by django and sent information about the request from client/browser/user. Display places & adds new places?
    if request.method == 'POST':
        #create new place
        form = NewPlaceForm(request.POST)#creating a form data that is sent in inputted request from user
        place = form.save(commit=False)#.save() creates a model object, or in this case a Place object? Checking for integrity error? commit=False means get data but don't save yet 
        place.user = request.user#assigns whatever user is making request, to be the owner of the Place? Idk
        if form.is_valid():#simple validation using the db constraints
            place.save() #committing the Place object to the db
            return redirect('place_list')#reloads/revisits the home page 
    
    #This is run if request is GET instead
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')#sending query to db. using filter instead of all, can send parameters with query. same with order_by
                        #^^first filter is using request object which has info of current user logged in, restrict to Places that belong to that user
    new_place_form = NewPlaceForm()#Empty NewPlaceForm that will be added dictionary for to homepage response
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})#combines template, list of places, and the form to create the response/webpage
    #^^sending information to template. render means combining the template with data. places dictionary has places list pulled out via query^^

@login_required
def about(request):
    author = 'Richard'
    about = 'A website created to display a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):#place_pk is variable pulling out the primary key associated with the visited place I think? Pks are autogenerated by the db
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)#db query. Pulling out single object that is being updated with POST. pk is the primary key db column.Will raise does not exist error if pk=something !exist
        place = get_object_or_404(Place, pk=place_pk)#django method. Needs the name of the class/model, and the db query. Will attempt get requests as normal, but if pk !exist, will return 404 error, will not crash
        if place.user == request.user:#checking is user allowed to make this request (Place belongs to that user?), if so make commits, then direct
            place.visited = True#Working only with the True values? Or does it change the visited Boolean?
            place.save()#ensuring the changes are committed
        else:
            return HttpResponseForbidden#if not allowed to make request, send this forbidden response

    return redirect('place_list')#reloads/revisits the home page. 
    #return redirect('places_visited)#Could be the name of another path to go somewhere else after the POST

@login_required
def place_details(request, place_pk):#place_pk is the captured stand-in in the respective urls.py path()
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html', {'place': place})#sending individual Place object



