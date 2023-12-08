

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,ClientSignUpForm
from datetime import date, datetime

from django.core.serializers import serialize


from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from .models import Client, Trainer,Message,Measurement,Subject,Movement,Nutrition,Food,Exercise

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string




def home(request):

    return render(request,"home.html")

def client_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_profile')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/client_login.html', {'form': form})

def trainer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('trainer_profile')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/trainer_login.html', {'form': form})

def client_dashboard(request):
    # Kullanıcı türüne bağlı olarak özel işlemler gerçekleştirilebilir.
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client

    return render(request, 'client_dashboard.html',{'client':client})

def trainer_dashboard(request):
    # Kullanıcı türüne bağlı olarak özel işlemler gerçekleştirilebilir.



    return render(request, 'trainer_dashboard.html')





def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        client_form = ClientSignUpForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            login(request, user)
            return redirect('home')  # veya başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        user_form = SignUpForm()
        client_form = ClientSignUpForm()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'client_form': client_form})


def dashboard(request):




    return render(request,'dashboard.html')



def profile(request):
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client
        email1=request.user.email

    if request.method == 'POST':
        birthday=request.POST.get('date')
        # email = request.POST.get('email')
        number = request.POST.get('number')
        image = request.FILES.get('profile')
        user=Client.objects.get(user__email=email1)
        user.image=image
        # user.user__email=email
        user.number=number
        user.birthday=birthday

        user.save()
        return redirect('client_profile')

    
    return render(request,'client/profile.html',{'client':client})

def trainer_profile(request):
    subjects=Subject.objects.all()
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        trainer = request.user.trainer
        email1=request.user.email

    if request.method == 'POST':
        # birthday=request.POST.get('date')
        # email = request.POST.get('email')
        number = request.POST.get('number')
        specialities = request.POST.get('specialities[]')
        image = request.FILES.get('profile')
        user=Trainer.objects.get(user__email=email1)
        user.image=image
        # user.user__email=email
        user.number=number
        for specialty in specialities:
            specialty=Subject.objects.get(id=specialty)
            user.speciality.add(specialty)
        

        user.save()
        return redirect('trainer_profile')

    
    return render(request,'trainer/profile.html',{'trainer':trainer,'subjects':subjects})


# def send_message(request):
#     if request.user.is_authenticated:
#         # Kullanıcının ilişkili Client modelini al
#         client = request.user.client
#         trainer=client.trainer

#         receiver = Client.objects.get(trainer=trainer)
#     if request.method == 'POST':
#         # form = MessageForm(request.POST)
#         # if form.is_valid():
#         #     content = form.cleaned_data['content']

#         Message.objects.create(sender=request.user, receiver=receiver, content=content)
#     return redirect('inbox')


def send_message(request):

    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client
        email1=request.user.email
    
        receiver=client.trainer.user.email

        sender=request.user
        receiver=User.objects.get(username=receiver)

    
    # receiver = User.objects.get(pk=receiver_id)
    if request.method == 'POST':
        # form = MessageForm(request.POST)

        mesagge_text=request.POST.get('message[]')

        # if form.is_valid():
        #     content = form.cleaned_data['content']
        message = Message.objects.create(sender=sender, receiver=receiver, content=mesagge_text)
        return redirect('send_message')  # Inbox sayfasına yönlendirme, uygun bir URL kullanmalısınız
    # else:
    #     form = MessageForm()
    messages=Message.objects.all()
    return render(request, 'client/inbox.html', {'receiver': receiver,'messages':messages})

def send_messageToClient(request):
    messages=Message.objects.all()
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        trainer = request.user.trainer
        email1=request.user.email
    
        sender=request.user

        
    
    if request.method == 'POST':
        # form = MessageForm(request.POST)
        receiver=request.POST.get('client')
        mesagge_text=request.POST.get('message[]')
        receiver=User.objects.get(id=receiver)
        # if form.is_valid():
        #     content = form.cleaned_data['content']
        message = Message.objects.create(sender=sender, receiver=receiver, content=mesagge_text)
        return redirect('trainer_inbox')
    clients=Client.objects.filter(trainer=trainer)
    # messages=Message.objects.filter(sender=sender)
    return render(request, 'trainer/inbox.html', {'clients': clients,'messages':messages})

# def trainer_inbox(request):
#     messages=Message.objects.all()
#     if request.user.is_authenticated:
#         # Kullanıcının ilişkili Client modelini al
#         trainer = request.user.trainer
#         email1=request.user.email

#     clients=Client.objects.filter(trainer=trainer)
#     return render(request,'trainer/inbox.html',{'clients':clients,'messages':messages})


# def inbox(request):
#     # user_profile = UserProfile.objects.get(user=request.user)
#     # messages = Message.objects.filter(receiver=request.user)
#     # return render(request, 'inbox.html', {'messages': messages, 'user_profile': user_profile})
#     return render(request,'client/inbox.html')



def program(request):
    
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client
        programs=client.exerciseProgram
        links=None
        if programs:
            links=[link for link in programs.monday.all()]
            links1=[link for link in programs.tuesday.all()]
            links2=[link for link in programs.wednesday.all()]
            links3=[link for link in programs.thursday.all()]
            links4=[link for link in programs.friday.all()]
    return render(request,'client/program.html',{'programs':programs,'links':links,'links1':links1,'links2':links2,'links3':links3,'links4':links4,})


def nutritionProgram(request):
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client
        diet=client.nutritionProgram

    return render(request,'client/nutritionprogram.html',{'diet':diet})

def progress(request):

    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        client = request.user.client
    
    if request.method=='POST':
        weigh=request.POST.get('weigh')
        height=request.POST.get('height')
        # proportion=request.POST.get('proportion')
        muscle=request.POST.get('muscle')
        # index=request.POST.get('index')
        today = datetime.now()
        index=float(weigh)/(float(float(height)/100)**2)
    
        today = datetime.now()
        birthday=client.birthday
    # Yaş hesaplama
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if client.gender=='erkek' :
            proportion=1.2*float(index)+0.23*int(age)-16.2
        else:
            proportion=1.2*float(index)+0.23*int(age)-5.4

        
        measurement=Measurement.objects.create(height=height,weight=weigh,rate=proportion,muscule=muscle,bodyindex=index)

        client.measurement.add(measurement)

    chart_data={
        'labels':[date.datenow.strftime('%Y-%m-%d') for date in client.measurement.all()],
        'height':[int(height.height)  for height in client.measurement.all()],
        'weight':[int(height.weight) for height in client.measurement.all() ],
        'rate':[int(height.rate) for height in client.measurement.all() ],
        'muscule':[int(height.muscule)for height in client.measurement.all() ],
        'bodyindex':[int(height.bodyindex)  for height in client.measurement.all()],

    }

    return render(request,'client/progressreport.html',{'client':client,'chart_data':chart_data})


    
def get_clients(request):
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        trainer = request.user.trainer

    clients=Client.objects.filter(trainer=trainer)


    return render(request,'trainer/clients.html',{'clients':clients})


def client_detail(request,client_id):

    client=Client.objects.get(id=client_id)

    measurement=client.measurement.all()
    measurement=serialize('json',measurement)
    diet=client.nutritionProgram
    return render(request,'trainer/client_detail.html',{'client':client,'measurement':measurement,'diet':diet})


def create_program(request):
    if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        trainer = request.user.trainer
    
        clients=Client.objects.filter(trainer=trainer)
        movements=Movement.objects.all()
        subjects=Subject.objects.all()
        if request.method=='POST':
            user_id=request.POST.get('client')
            monday1=request.POST.get('radio1')
            monday1=Movement.objects.get(id=monday1)
            monday2=request.POST.get('radio6')
            monday2=Movement.objects.get(id=monday2)
            monday3=request.POST.get('radio11')
            monday3=Movement.objects.get(id=monday3)
            tuesday1=request.POST.get('radio2')
            tuesday1=Movement.objects.get(id=tuesday1)
            tuesday2=request.POST.get('radio7')
            tuesday2=Movement.objects.get(id=tuesday2)
            tuesday3=request.POST.get('radio12')
            tuesday3=Movement.objects.get(id=tuesday3)
            wednesday1=request.POST.get('radio3')
            wednesday1=Movement.objects.get(id=wednesday1)
            wednesday2=request.POST.get('radio8')
            wednesday2=Movement.objects.get(id=wednesday2)
            wednesday3=request.POST.get('radio13')
            wednesday3=Movement.objects.get(id=wednesday3)
            thursday1=request.POST.get('radio4')
            thursday1=Movement.objects.get(id=thursday1)
            thursday2=request.POST.get('radio9')
            thursday2=Movement.objects.get(id=thursday2)
            thursday3=request.POST.get('radio14')
            thursday3=Movement.objects.get(id=thursday3)
            friday1=request.POST.get('radio5')
            friday1=Movement.objects.get(id=friday1)
            friday2=request.POST.get('radio10')
            friday2=Movement.objects.get(id=friday2)
            friday3=request.POST.get('radio15')
            friday3=Movement.objects.get(id=friday3)
            start_date=request.POST.get('start_date')
            end_date=request.POST.get('end_date')
            subject_id=request.POST.get('subject')
            subject=Subject.objects.get(id=subject_id)

            client=Client.objects.get(user__id=user_id)
            newprogram=Exercise.objects.create(name=subject.name,purpose=subject,start_date=start_date,end_date=end_date)
            newprogram.monday.add(monday1,monday2,monday3)
            newprogram.tuesday.add(tuesday1,tuesday2,tuesday3)
            newprogram.wednesday.add(wednesday1,wednesday2,wednesday3)
            newprogram.thursday.add(thursday1,thursday2,thursday3)
            newprogram.friday.add(friday1,friday2,friday3)
            newprogram.save()
            client.exerciseProgram=newprogram
            client.save()
            
        return render(request,'trainer/createprogram.html',{'movements':movements,'clients':clients,'subjects':subjects})


def create_nutrition(request):
     if request.user.is_authenticated:
        # Kullanıcının ilişkili Client modelini al
        trainer = request.user.trainer
    
        clients=Client.objects.filter(trainer=trainer)
        foods=Food.objects.all()
        if request.method=='POST':
            user_id=request.POST.get('client')
            monday1=request.POST.get('radio1')
            monday1=Food.objects.get(id=monday1)
            monday2=request.POST.get('radio6')
            monday2=Food.objects.get(id=monday2)
            monday3=request.POST.get('radio11')
            monday3=Food.objects.get(id=monday3)
            tuesday1=request.POST.get('radio2')
            tuesday1=Food.objects.get(id=tuesday1)
            tuesday2=request.POST.get('radio7')
            tuesday2=Food.objects.get(id=tuesday2)
            tuesday3=request.POST.get('radio12')
            tuesday3=Food.objects.get(id=tuesday3)
            wednesday1=request.POST.get('radio3')
            wednesday1=Food.objects.get(id=wednesday1)
            wednesday2=request.POST.get('radio8')
            wednesday2=Food.objects.get(id=wednesday2)
            wednesday3=request.POST.get('radio13')
            wednesday3=Food.objects.get(id=wednesday3)
            thursday1=request.POST.get('radio4')
            thursday1=Food.objects.get(id=thursday1)
            thursday2=request.POST.get('radio9')
            thursday2=Food.objects.get(id=thursday2)
            thursday3=request.POST.get('radio14')
            thursday3=Food.objects.get(id=thursday3)
            friday1=request.POST.get('radio5')
            friday1=Food.objects.get(id=friday1)
            friday2=request.POST.get('radio10')
            friday2=Food.objects.get(id=friday2)
            friday3=request.POST.get('radio15')
            friday3=Food.objects.get(id=friday3)

            client=Client.objects.get(id=user_id)

            newprogram=Nutrition.objects.create(name=client.user.username)
            newprogram.monday.add(monday1,monday2,monday3)
            newprogram.tuesday.add(tuesday1,tuesday2,tuesday3)
            newprogram.wednesday.add(wednesday1,wednesday2,wednesday3)
            newprogram.thursday.add(thursday1,thursday2,thursday3)
            newprogram.friday.add(friday1,friday2,friday3)
            newprogram.save()
            client.nutritionProgram=newprogram
            client.save()

        return render(request,'trainer/createnutrition.html',{'foods':foods,'clients':clients})

