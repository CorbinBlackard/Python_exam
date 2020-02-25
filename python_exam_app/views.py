from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
import bcrypt
from django.db.models import Count

def index(request):
    return render(request, "login_reg.html")

def createUser(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            print("User's password entered was " + request.POST['password'])
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
            print("User's password has been changed to " + user.password)
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id #IMPORTANT!!!
                return redirect('/homepage')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Name not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def homepage(request):
    if "user_id" in request.session:
        context = {
            "all_users": User.objects.get(id=request.session['user_id']),
            "all_quotes": Quote.objects.all()
        }
        return render(request, "home_page.html", context)
    else: 
        return redirect('/')

def logged_out(request):
    if request.session['user_id']:
        request.session.clear()
    return redirect('/')

def createQuote(request):
    if "user_id" in request.session:
        if request.method == "POST":
            errors = Quote.objects.quote_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            else:
                quote = Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], user=User.objects.get(id=request.session['user_id']))
        return redirect('/homepage')
    else:
        return redirect('/')

def likeQuote(request, quote_id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=quote_id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.users_that_liked.add(user)
    return redirect('/homepage')

def unlikeQuote(request, quote_id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=quote_id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.users_that_liked.remove(user)
    return redirect('/homepage')

def deleteQuote(request, quote_id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=quote_id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            if quote.user == user:
                quote.delete()
    return redirect('/homepage')

def profile(request, user_id):
    if "user_id" in request.session:
        context = {
            "user": User.objects.get(id=user_id),
            "all_quotes": Quote.objects.all()
        }
        return render(request, "profile.html", context)
    else:
        return redirect('/')

def editPage(request):
    if "user_id" in request.session:
        context = {
            "edit_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'edit_page.html', context)
    else:
        return redirect('/')

def updateInfo(request):
    if request.method == "POST":
        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(id=request.session['user_id'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
    return redirect('/editPage/')
