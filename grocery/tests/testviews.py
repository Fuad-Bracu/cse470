from django.test import TestCase,Client
from django.urls import reverse,resolve
from grocery.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.contrib.auth.models import User
import json
from django.core.files import File

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestViews(TestCase):

	def setUp(self):
		self.client = Client()
		



	def test_home_views(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'all_product.html')


	def test_signup_views_get(self):
		response = self.client.get(reverse('signup'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'signup.html')

	def test_signup_views_post(self):
		
		with open('grocery/tests/img.jpg','rb') as imgfile:
			
			response = self.client.post(reverse('signup'),
				{'fname':'testname',
				'lname':'testlname',
				'uname':'testuname',
				'pwd':'testpwd',
				'date':'2021-05-22',
				'city':'dhaka',
				'add':'testadd',
				'email':'testefail@gmail.com',
				'img':imgfile,
				'contact':'testcontact',


				})
			self.assertEquals(response.status_code,200)



	def test_about_views(self):
		response = self.client.get(reverse('about'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'about.html')



	def test_contact_views(self):
		response = self.client.get(reverse('contact'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'contact.html')



	def test_login_views_get(self):
		response = self.client.get(reverse('login'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'login.html')



	def test_login_views_post(self):
		response = self.client.post(reverse('login'),{'uname':'testuname','pwd':'testpwd'})
		self.assertEquals(response.status_code,200)

	def test_logout_views(self):
		response = self.client.get(reverse('logout'))
		self.assertEquals(response.status_code,302)

	def test_view_user(self):
		response = self.client.get(reverse('view_user'))
		self.assertEquals(response.status_code,302)

	def test_add_product_get(self):
		response = self.client.get(reverse('add_product'))
		self.assertEquals(response.status_code,302)

	def test_add_product_post(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		with open('grocery/tests/img.jpg','rb') as imgfile:
			Category.objects.create(name='testcat')
			response = self.client.post(reverse('add_product'),
				{'cat':'testcat',
				'pname':'testp',
				'price':'12',
				'desc':'test',

				'img':imgfile,
				'contact':'testcontact',


				})
			self.assertEquals(response.status_code,200)


	def test_view_feedback(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		response = self.client.get(reverse('view_feedback'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'view_feedback.html')


	def test_view_product(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		Category.objects.create(name='testcat')
		Profile.objects.create(user = self.user)
		response = self.client.get(reverse('view_product',args=[1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'view_product.html')




	def test_admin_view_product(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		Profile.objects.create(user = self.user)
		#Product.objects.create(category=cat)
		response = self.client.get(reverse('admin_view_product'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'admin_view_product.html')





	
	def test_login_admin_get(self):
		self.user = User.objects.create(username='testuser',is_staff=True)
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		
		Category.objects.create(name='testcat')
		response = self.client.post(reverse('login_admin'),
				{'uname':'testuser',
				'pwd':'12345'
				
				})
		self.assertEquals(response.status_code,200)




	def test_admin_view_booking(self):
		self.user = User.objects.create(username='testuser',is_staff=True)
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		response = self.client.get(reverse('admin_viewBooking'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'admin_viewBokking.html')

		


	def test_view_category(self):
		self.user = User.objects.create(username='testuser',is_staff=True)
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		response = self.client.get(reverse('view_categary'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'view_category.html')




	def test_add_category(self):
		self.user = User.objects.create(username='testuser',is_staff=True)
		self.user.set_password('12345')
		self.user.save()
		self.client.login(username='testuser', password='12345')
		response = self.client.post(reverse('add_categary'),{'cat':'testcat'})
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'add_category.html')



	def test_add_cart(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		Profile.objects.create(user = self.user)
		Product.objects.create(category = cat)
		response = self.client.post(reverse('add_cart',args=[1]))
		self.assertEquals(response.status_code,302)
		


	def test_delete_product(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		Profile.objects.create(user = self.user)
		Product.objects.create(category = cat)
		response = self.client.get(reverse('delete_product',args=[1]))
		self.assertEquals(response.status_code,302)



	def test_delete_user(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		Profile.objects.create(user = self.user)
		Product.objects.create(category = cat)
		response = self.client.get(reverse('delete_user',args=[1]))
		self.assertEquals(response.status_code,302)



	def test_delete_feedback(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		p=Profile.objects.create(user = self.user)
		Send_Feedback.objects.create(profile=p)
		Product.objects.create(category = cat)

		response = self.client.get(reverse('delete_feedback',args=[1]))
		self.assertEquals(response.status_code,302)


	def test_view_cart(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		p=Profile.objects.create(user = self.user)
		Send_Feedback.objects.create(profile=p)
		Product.objects.create(category = cat)

		response = self.client.get(reverse('cart'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'cart.html')


	def test_payment(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		cat=Category.objects.create(name='testcat')
		p=Profile.objects.create(user = self.user)
		Send_Feedback.objects.create(profile=p)
		Product.objects.create(category = cat)

		response = self.client.get(reverse('payment',args=[1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'payment2.html')



	def test_delete_booking(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		
		p=Profile.objects.create(user = self.user)
		Booking.objects.create(booking_id=1)
		

		response = self.client.get(reverse('delete_booking',args=[1,1]))
		self.assertEquals(response.status_code,302)


	def test_delete_admin_booking(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		
		p=Profile.objects.create(user = self.user)
		Booking.objects.create(booking_id=1)
		

		response = self.client.get(reverse('delete_admin_booking',args=[1,1]))
		self.assertEquals(response.status_code,302)



	def test_get_booking_details(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		
		p=Profile.objects.create(user = self.user)
		Booking.objects.create(booking_id=1)
		

		response = self.client.get(reverse('booking_detail',args=[1,1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'booking_detail.html')



	def test_get_admin_booking_details(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))

		p=Profile.objects.create(user = self.user,image=img)
		Booking.objects.create(booking_id=1)
		

		response = self.client.get(reverse('admin_booking_detail',args=[1,1,1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'admin_view_booking_detail.html')	



	def test_get_edit_status(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='testname')
		p=Profile.objects.create(user = self.user,image=img)
		Booking.objects.create(booking_id=1)
		

		response = self.client.get(reverse('Edit_status',args=[1,1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'status.html')




	def test_post_edit_status(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='testname')
		p=Profile.objects.create(user = self.user,image=img)
		Booking.objects.create(booking_id=1)
		

		response = self.client.post(reverse('Edit_status',args=[1,1]),{'book':1,'status':'testname'})
		self.assertEquals(response.status_code,302)
		



	def test_remove_cart(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='testname')
		p=Profile.objects.create(user = self.user,image=img)
		Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		Cart.objects.create(profile=p,product=pro)

		response = self.client.get(reverse('remove_cart',args=[1]))
		self.assertEquals(response.status_code,302)


	def test_booking_order_get(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='testname')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		cart=Cart.objects.create(profile=p,product=pro)

		response = self.client.get(reverse('booking',args=[1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'booking.html')



	def test_booking_order_post(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		cart=Cart.objects.create(profile=p,product=pro)

		response = self.client.post(reverse('booking',args=[1]),
			{

			'date1':'2021-05-18',
			'name':'testuser',
			'city':'testcity',
			'add':'testadd',
			'email':'testemail@gmail.com',
			'contact':'test contact',
			'book_id':1,
			'total':23

			})
		self.assertEquals(response.status_code,302)
		



	def test_view_booking(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		#Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		cart=Cart.objects.create(profile=p,product=pro)

		response = self.client.get(reverse('view_booking'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'view_booking.html')


	def test_profile_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		Cart.objects.create(profile=p,product=pro)

		response = self.client.get(reverse('profile'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'profile.html')



	def test_edit_profile_view_get(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		Cart.objects.create(profile=p,product=pro)

		response = self.client.get(reverse('edit_profile'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'edit_profile.html')



	def test_edit_profile_post_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		cart=Cart.objects.create(profile=p,product=pro)

		response = self.client.post(reverse('edit_profile'),
			{

			'fname':'testuser',
			'uname':'testuname',
			'lname':'testlname',
			'city':'testcity',
			'add':'testadd',
			'email':'testemail@gmail.com',
			'contact':'testcontact',
			'date':'2021-05-18'

			})
		self.assertEquals(response.status_code,200)




	def test_delete_catagory_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		Category.objects.create(name='test category')
		book=Booking.objects.create(booking_id=1)
	

		response = self.client.get(reverse('delete_category',args=[1]))
		self.assertEquals(response.status_code,302)
		


	def test_admin_home_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		Category.objects.create(name='test category')
		book=Booking.objects.create(booking_id=1)
	

		response = self.client.get(reverse('admin_home'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'admin_home.html')


	def test_change_password_get_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		#Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		Category.objects.create(name='test category')
		book=Booking.objects.create(booking_id=1)
	

		response = self.client.get(reverse('change_password'))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'change_password.html')

	def test_feedback_get_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		#Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		Category.objects.create(name='test category')
		book=Booking.objects.create(booking_id=1)
	

		response = self.client.get(reverse('send_feedback',args=[1]))
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'feedback.html')


	def test_feedback_post_view(self):
		self.user = User.objects.create(username='testuser')
		self.user.set_password('12345')
		self.user.save()
		logged=self.client.login(username='testuser', password='12345')
		img=File(open('grocery/tests/img.jpg', 'rb'))
		Status.objects.create(name='pending')
		p=Profile.objects.create(user = self.user,image=img)
		book=Booking.objects.create(booking_id=1)
		pro = Product.objects.create(image=img)
		cart=Cart.objects.create(profile=p,product=pro)

		response = self.client.post(reverse('send_feedback',args=[1]),
			{

			'desc':'testdesc',
			'uname':'testuname',
		
			
			'email':'testemail@gmail.com',
			'contact':'testcontact',
			'date':'2021-05-18'

			})
		self.assertEquals(response.status_code,200)