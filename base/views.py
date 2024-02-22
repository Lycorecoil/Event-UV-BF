from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib .auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Topic, Message
from .forms import EvenForm, UserForm




#events =[
#	{'id':1, 'name':'Michael jackson event'},
#	{'id':2, 'name':'Bob marley event'},
#	{'id':3, 'name':'Avenger event'},
#]
	
# Create your views here.

def loginPage(request):
	page = 'login'

	if request.user.is_authenticated:
		return redirect('home')



	if request.method == "POST":
		username = request.POST.get('username').lower()
		password = request.POST.get('password')

		try:
			user = User.objects.get(username = username)
		except:
			messages.error(request,'User does not exist woo')

		user = authenticate(request, username = username, password =password)

		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.error(request,'username ou password does not exit')

	context = {'page':page}
	return render(request, 'base/login_register.html', context)




def logoutUser(request):
	logout(request)
	return redirect('home')




def registerPage(request):
	form =  UserCreationForm()

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			login(request,user)
			return redirect('home')
		else:
			messages.error(request,"Erreur lors de l'enregistrement")

	context = {'form':form}
	return render(request,'base/login_register.html',context)




def home(request):
	q = request.GET.get('q') if request.GET.get('q')!=None else ''
	events = Event.objects.filter(
		                          Q(topic__name__icontains=q)|
							      Q(title__icontains=q)|
								  Q(description__icontains=q)
								 )
	topics = Topic.objects.all()
	event_count = Event.objects.all().count()
	print(event_count)
	event_messages = Message.objects.filter(Q(event__topic__name__icontains=q))



	context={'events':events,'topics':topics,'event_count':event_count,'event_messages':event_messages}
	return render(request,'base/home.html',context)




def event(request,pk):
	event = Event.objects.get(id=pk)
	event_messages = event.message_set.all()

	participants = event.participants.all()

	if request.method=="POST":
		message = Message.objects.create(
			user = request.user,
			event= event,
			body = request.POST.get('body'),
		)
		return redirect('event',pk=event.id)

	context={'event':event,'event_messages':event_messages,'participants':participants}
	return render(request,'base/event.html',context)



def userProfile(request,pk):
	user = User.objects.get(id=pk)
	events = user.event_set.all()
	event_messages = user.message_set.all()
	topics = Topic.objects.all()
	context = {'user':user,'events':events,'event_messages':event_messages,'topics':topics}
	return render(request,"base/profile.html",context)



@login_required(login_url = 'login')
def createEvent(request):
	form = EvenForm()
	topics = Topic.objects.all()
	if request.method == "POST":
		form = EvenForm(request.POST, request.FILES)
		topic_name =request.POST.get('topic')
		topic, create = Topic.objects.get_or_create(name=topic_name)

		Event.objects.create(
			host =request.user,
			topic = topic,
			title = request.POST.get('title'),
			description = request.POST.get('description'),
			date = request.POST.get('date'),
			image = request.FILES.get('image'),
			
		)
#		
		return redirect('home')

	context ={"form":form,'topics':topics}
	return render(request,'base/event_form.html',context)



@login_required(login_url = 'login')
def updateEvent(request,pk):
	event = Event.objects.get(id=pk)
	form = EvenForm(instance=event)
	topics = Topic.objects.all()

	if request.user != event.host:
		return HttpResponse("C'est pas ton evenement")

    

	if request.method == "POST":
		topic_name =request.POST.get('topic')
		topic, create = Topic.objects.get_or_create(Name=topic_name)
		form = EvenForm(request.POST,instance=event)
		event.title = request.POST.get('title')
		event.topic = topic
		event.description = request.POST.get('description')
		event.save()
		return redirect('home')
		
	context ={"form":form,'topics':topics,'event':event}
	return render(request,'base/event_form.html',context)



@login_required(login_url='login')
def deleteEvent(request,pk):
	event = Event.objects.get(id=pk)
	if request.user != event.host:
		return HttpResponse("Seule l'admin peut le supprimer")
	if request.method == "POST":
		event.delete()
		return redirect('home')
	context ={'obj':event.title}
	return render(request,'base/delete.html',context)




@login_required(login_url='login')
def deleteMessage(request,pk):
	message = Message.objects.get(id=pk)
	if request.user != message.user:
		return HttpResponse("C'est pas ton evenement")
	if request.method == "POST":
		message.delete()
		return redirect('home')
	context ={'obj':message}
	return render(request,'base/delete.html',context)


@login_required(login_url='login')
def updateUser(request):
	user = request.user
	print(user)
	form = UserForm(instance=request.user)
	if request.method == "POST":
		
		form = UserForm(request.POST,instance=user)
		
		if form.is_valid():
			
			form.save()
			
			return redirect('user-profile',pk=user.id)
		else:
			print("non valid")
	
	return render(request,"base/update-user.html",{'form':form})