import json
from .models import *
import string
import random

def cookieCart(request):
  #Criar carrinho vazio por enquanto para usuário não logado
  try:
    cart = json.loads(request.COOKIES['cart'])
  except:
    cart = {}
    
  #print('cart:', cart)
  items = []
  order = {'get_cart_total':0, 'get_cart_items':0}
  cartItems = order['get_cart_items']
  
  for i in cart: 
    #Usamos try block para evitar que itens no carrinho que possam ter sido removidos causem erro
    try:
      cartItems += cart[i]["quantity"]
  
      product = Product.objects.get(id=i)
      total = (product.price * cart[i]['quantity'])
  
      order['get_cart_total'] += total
      order['get_cart_items'] += cart[i]['quantity']
  
      item = {
    		'product':{
    			'id':product.id,
    			'name':product.name, 
    			'price':product.price, 
    			'imageURL':product.imageURL
    			}, 
    		'quantity':cart[i]['quantity'],
    		'get_total':total,
  		}
      items.append(item)
        
      if product.digital == False:
  	    shipping = True
        
    except:
       pass
      
  return {'cartItems':cartItems ,'order':order, 'items':items}
  
def cartData(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    
  return{'cartItems':cartItems ,'order':order, 'items':items}
  
def guestOrder(request, data):
  name = data['form']['name']
  email = data['form']['email']

  cookieData = cookieCart(request)
  #print(cookieData)
  items = cookieData['items']

  customer, created = Customer.objects.get_or_create(
			email=email,
			)
  customer.name = name
  customer.save()

  order = Order.objects.create(
		customer=customer,
		complete=False,
    )

  for item in items:
    product = Product.objects.get(id=item['product']['id'])
    orderItem = OrderItem.objects.create(
      product=product,
      order=order,
      quantity=item['quantity'],
		)
    
  return customer, order
  
def welcomeMsg(user):
  return "Olá " + user.first_name + ",\nEstou enviando esta mensagem para agradecer por criar uma conta e dizer que você é muito bem-vindo(a) à nossa loja.\n\nGarantimos que sua estadia será excelente!\n\nNipponime Staff"
  
def newGestUserMsg(customer, usuarioo, password):
  return '\n' + customer.name + ', Criamos um usuario para si\n\n ' + '\n\nLogin: ' + usuarioo + '\nPassword: ' + password + '\nEmail: ' + customer.email + '.\n\n\nObrigado pelo sua preferência,\nNIPPONIME 2023'
  
def newOrderMsg(customer, data):
  return '\n' + customer.name + ', Obrigado por comprar na nossa loja\n\nIrá ser enviado a sua compra em breve.\nProcessaremos encomenda para a ' + str(data['shipping']['city']) + '.\n\n\nObrigado pelo sua preferência,\nNIPPONIME 2023'

def get_random_string(length):
    # choose from The concatenation of the ascii_lowercase and ascii_uppercase constants described below. This value is not locale-dependent.
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str