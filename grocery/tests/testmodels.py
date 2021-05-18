from django.test import TestCase 
from django.urls import reverse,resolve
from grocery.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.contrib.auth.models import User
import json
from django.core.files import File



class TestModels(TestCase):

	def setUp(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		self.logged=self.client.login(username='testuser', password='12345')
		self.img=File(open('grocery/tests/img.jpg', 'rb'))




	def test_category_model(self):
		new_cat=Category.objects.create(name='testcat')
		self.assertEquals(new_cat.name,'testcat')
		new_cat.delete()
		self.assertEquals(Category.objects.all().count(),0)



	def test_product_model(self):
		cat=Category.objects.create(name='testcat')
		new_prod = Product.objects.create(category=cat,image=self.img,name='testname',price=10,desc='testdesc')
		check= Product.objects.get(id=1)
		self.assertEquals(check.name,'testname')
		new_prod.delete()
		self.assertEquals(Product.objects.all().count(),0)


	def test_status_model(self):
		st=Status.objects.create(name='test status')

		self.assertEquals(st.name,'test status')
		st.delete()
		self.assertEquals(Status.objects.all().count(),0)



	def test_profile_model(self):

		pro = Profile.objects.create(

			user = self.user,
			dob='2021-05-18',
			city='testcity',
			address='testaddr',
			contact='testcontact',
			image = self.img


			)


		self.assertEquals(pro.city,'testcity')

		pro.delete()

		self.assertEquals(Profile.objects.all().count(),0)



	def test_cart_model(self):
		c=Category.objects.create(name='testcat')
		P=Product.objects.create(category=c)
		pro = Profile.objects.create(user=self.user)
		cart=Cart.objects.create(profile=pro,product=P)

		self.assertEquals(cart.product.category.name,'testcat')

		cart.delete()

		self.assertEquals(Cart.objects.all().count(),0)



	def test_booking_model(self):
		create_status = Status.objects.create(name='testname')
		pro = Profile.objects.create(user=self.user)

		booking_ins = Booking.objects.create(status=create_status,profile=pro,booking_id='1',quantity='1',book_date='2021-05-18',total=200)


		self.assertEquals(booking_ins.booking_id,'1')

		booking_ins.delete()

		self.assertEquals(Booking.objects.all().count(),0)



	def test_send_feedback_model(self):
		pro = Profile.objects.create(user=self.user)

		feedback=Send_Feedback.objects.create(profile=pro,message1='testmsg',date='2021-05-18')

		self.assertEquals(feedback.message1,'testmsg')

		feedback.delete()

		self.assertEquals(Send_Feedback.objects.all().count(),0)

