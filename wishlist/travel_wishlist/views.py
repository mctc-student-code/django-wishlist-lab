from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required#ensuring views are only visible while logged in


"""Views are the controller, sending specific responses to be displayed"""
@login_required
def place_list(request):#function takes only request argument. Will be called by django and sent information about the request from client/browser/user. Display places & adds new places?
    if request.method == 'POST':
        #create new place
        form = NewPlaceForm(request.POST)#creating a form data that is sent in inputted request from user
        place = form.save()#.save() creates a model object, or in this case a Place object?
        if form.is_valid():#simple validation using the db constraints
            place.save() #committing the Place object to the db
            return redirect('place_list')#reloads/revisits the home page 
    
    #This is run if request is GET instead
    places = Place.objects.filter(visited=False).order_by('name')#sending query to db. using filter instead of all, can send parameters with query. same with order_by
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
def place_was_visited(request, place_pk):#place_pk is variable pulling out the priomary key associcated with the visited place I think? Pks are autogenerated by the db
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)#db query. Pulling out single object that is being updated with POST. pk is the primary key db column.Will raise does not exist error if pk=something !exist
        place = get_object_or_404(Place, pk=place_pk)#django method. Needs the name of the class/model, and the db query. Will attempt get requests as normal, but if pk !exist, will return 404 error, not crash
        place.visited = True#Working only with the True values? Or does it change the visited Boolean?
        place.save()#ensuring the changes are committed

    return redirect('place_list')#reloads/revisits the home page. 
    #return redirect('places_visited)#Could be the name of another path to go somewhere else after the POST


