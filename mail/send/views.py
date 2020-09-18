from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from send.models import (
    Profile,
)
# Create your views here.
def index(request):
    return render(request,'index.html')

def login_view(request):

    if request.user.is_authenticated:
        return render(request,'index.html')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,
                            password=password)
        
        if user is not None:
            login(request,user)
            return render(request,'index.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request,'index.html')

@login_required
def profile_upload(request):
    # declaring template
    template = "profile_upload.html"
    data = Profile.objects.all()
    
    prompt = {
        'order': 'Order of the CSV should be name, email, address, phone, profile',
        'profiles': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Profile.objects.update_or_create(
            name=column[0],
            email=column[1],
            address=column[2],
            phone=column[3],
            profile=column[4]
        )
    data = Profile.objects.all()
    context = {"profiles":data,
                'messages': ['Your File has been succesfully Uploaded']}
    return render(request, template, context)


@login_required    
def send_view(request):

    data = Profile.objects.all()
    template = 'send.html'

    if request.POST:
        connection = mail.get_connection()

        # Manually open the connection
        connection.open()

        # Construct an email message that uses the connection
        email1 = mail.EmailMessage(
            'Hello',
            'Hwy there how you doing',
            'from@example.com',
            ['amanjn315@gmail.com'],
            connection=connection,
        )
        email1.send() # Send the email
        connection.close()

        context = {'messages':'Mail is send succesfully to "amanjn315@gmail.com"'}
        return render(request,template,context) 

    else:
        context = {"profiles":data}
        return render(request,template,context)
    return render(request,template)
