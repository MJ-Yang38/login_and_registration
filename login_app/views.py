import re
from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,"index.html")
# register function here
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        if request.method=="POST":
            pword = request.POST['password']
            pw_hash = bcrypt.hashpw(pword.encode(), bcrypt.gensalt()).decode()  
            User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
        return redirect('/')
#login function here, first redirect then render a success page        
def login(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.filter(email=request.POST['user_email']) 
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        #indentation here is very important as only follows through if user[0] exists!!!!!!
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            #request.session['useremail'] = logged_user.email
            #request.session['userfirstname']=logged_user.first_name
            return redirect('/success')
    #error message shows if login isn't successful        
    messages.error(request, "Login Failed!")
    return redirect('/')
#success page will be replaced by the wall page within just one app.#
#####################################################################
def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)

#Have the logout link clear the session and redirect to the login/reg page
def logout(request):
    request.session.flush() #what's the difference between this and clear()?
    return redirect('/')

