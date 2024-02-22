from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
	name=models.CharField(max_length=32)

	def __str__(self):
		return self.name

class Event(models.Model):
	host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=32)
	description = models.TextField(null=True,blank=True)
	participants = models.ManyToManyField(User, related_name='participants',blank=True)
	image = models.ImageField(upload_to='images/',null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated','-created']

	def __str__(self):
		return self.title
	
class Message(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	event= models.ForeignKey(Event,on_delete=models.CASCADE)
	body = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-updated','-created']

	def __str__(self):
		return self.body[0:50]

