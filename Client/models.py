from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Myuser(models.Model):
	user = models.OneToOneField(User)
	permission = models.IntegerField()

class Dish(models.Model):
	name = models.CharField(max_length=128)
	price = models.FloatField()
	typ = models.CharField(max_length=128)
	intro = models.TextField()
	count = models.IntegerField()

	def __init__(self):
		self.count = 0

class Img(models.Model):
	image = models.ImageField(upload_to='photos')
	intro = models.TextField()
	dish = models.ForeignKey(Dish)

class Desk(models.Model):
	ip = models.IPAddressField()
	num = models.IntegerField()

class Order(models.Model):
	dish = models.ManyToManyField(Dish)
	paied = models.IntegerField()
	pub_date=models.DateField()
	desk = models.ForeignKey(Desk)

	def __init__(self):
		self.paied = 0 

class Remark(models.Model):
	client = models.ForeignKey(Myuser)
	content = models.TextField()
	dish = models.ForeignKey(Dish)
	pub_date = models.DateField()