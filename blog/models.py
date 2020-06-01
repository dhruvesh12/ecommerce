from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RegisterType(models.Model):
	name=models.CharField(max_length=200)

	def __str__(self):
		return self.name



class Register(models.Model):
	f_name=models.OneToOneField(User, on_delete=models.CASCADE)
	#l_name=models.CharField(max_length=200)
	add=models.CharField(max_length=200)
	phone=models.CharField(max_length=10)
	types=models.ForeignKey(RegisterType,on_delete=models.CASCADE,null=True)


	def __str__(self):
		return self.f_name.username


class FoodType(models.Model):
	name=models.CharField(max_length=200)

	def __str__(self):
		return self.name



class Food(models.Model):
	name=models.CharField(max_length=200)
	food_img=models.ImageField(upload_to='food_image/')
	types=models.ForeignKey(FoodType,on_delete=models.CASCADE)
	price = models.IntegerField(default=0)

	def __str__(self):
		return self.name




class Restaurant(models.Model):
	owner=models.ForeignKey(Register,on_delete=models.CASCADE)
	name=models.CharField(max_length=200)
	address = models.CharField(max_length=80)
	product_image=models.ImageField(upload_to='rest_img/')
	#phoneNumber = models.CharField(max_length=10)
	recipe = models.ManyToManyField(Food,blank=True)

	def __str__(self):
		return self.name


class Orders(models.Model):
	order_id=models.IntegerField(default=0)
	Restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	From_order=models.ForeignKey(User, on_delete=models.CASCADE)
	order=models.ManyToManyField(Food,blank=True)
	status=models.BooleanField(default=True)

	#def publish(self):
	#	self.From_order = timezone.now()
	#	self.save()

	#def get_total(self):


	def __str__(self):
		total = 0
		for order_item in self.order.all():
			#print(order_item)
			total += order_item.price

		return str(total)
		#return "you got order From {}".format(self.From_order)
		#return Orders.objects.filter(order.name=self.order)

