from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('blog', views.blog, name="blog"),
	path('contact', views.contact, name="contact"),
	path('web', views.web, name="web"),
	path('member', views.member, name="member"),
	path('gallery', views.gallery, name="gallery"),
	path('signup', views.handlesignup, name="handlesignup"),
	path('login', views.handlelogin, name="handlelogin"),
	path('logout', views.handlelogout, name="handlelogout"),


]