from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.core.signals import request_finished
from django.dispatch import receiver, Signal
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	paginator = Paginator(products,3)
	page= request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	context = {'page': page,'products': products, 'cartItems': cartItems,}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def blog(request):
    return render(request, 'store/blog.html')

def contact(request):
    return render(request, 'store/contact.html')

def web(request):
    return render(request, 'store/web.html')

def member(request):
    return render(request, 'store/member.html')

def gallery(request):
    return render(request, 'store/gallery.html')

def handlesignup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        city = request.POST['city']
        state = request.POST['state']
        postalcode = request.POST['postalcode']

        # check for anny error
        if pass1 != pass2:
            messages.error(request, 'your passwords do not match')
            return redirect('/')

        # create the user
        myuser = User.objects.create_user(username=username, email=username, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'your account has been created successfully')

        return redirect('/')

    else:
        return HttpResponse("404 not found")

@receiver(request_finished)
def func(sender,**kwargs):
	print("request finished")


def handlelogin(request):
    if request.method == 'POST':
        # get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In!!!')
            return redirect('/')
        else:
            messages.error(request, 'You Have Entered Invalid Credentials, Please Try Again!!!')

        return redirect('/')
    return HttpResponse("404 not found")


def handlelogout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('/')

