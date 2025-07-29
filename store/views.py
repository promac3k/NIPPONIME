from django.shortcuts import render, redirect
from .models import *  
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder, welcomeMsg, newOrderMsg, newGestUserMsg, get_random_string
from .forms import NewUserForm, ClientForm, ContactForm
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
import math
from django.core.mail import send_mail
from django.conf import settings
import random
from django.db.models import Q

def store(request):
  if request.user.is_authenticated: 
    cliente = request.user.customer
  else:
    cliente = {}
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  products = Product.objects.filter(is_promo=False).order_by('-tag')
  # aleatoriamnete 2 items só
  # import random
  items = list(Product.objects.filter(is_promo=True).exclude(tag__name__contains="Esgotado"))
  promos = random.sample(items, 2)
  #promos = Product.objects.filter(is_promo=True)
  category = Category.objects.all()

  paginator = Paginator(products, 9) # Mostrar 9 produtos por página.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  
  context = {'page_obj':page_obj, 'products':products, 'cartItems':cartItems, 'category':category, 'customer':cliente, 'promos':promos}
  return render(request, 'store/Store.html', context)
  
def cart(request):
  
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']

  context = {'items':items, 'order':order, 'cartItems':cartItems}
  return render(request, 'store/Cart.html', context)
  
def checkout(request):
  if request.user.is_authenticated: 
    cliente = request.user.customer
  else:
    cliente = {}
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
    
  context = {'items':items, 'order':order, 'customer':cliente, 'cartItems':cartItems}
  return render(request, 'store/Checkout.html', context)
  
def updateItem(request):
  print(request.body)
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  quant = int(data['quant'])
  print('Action:', action)
  print('Product:', productId)
  
  customer = request.user.customer
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
  
  if action == 'add':
    orderItem.quantity = (orderItem.quantity + quant)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - quant)
    
  orderItem.save()
  
  if orderItem.quantity <= 0:
    orderItem.delete()
    
  return JsonResponse('O item foi adicionado', safe=False)
  
def processOrder(request):
  
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)
  criado_usuario = False
  #print(data)
  
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #print(">>>>>>>>>> ",order)
  else:
    customer, order = guestOrder(request, data)
    try:
      #vamos criar no user? mas antes temos de verificar se existe e não está logado!
      password = get_random_string(16)
      usuarioo = customer.name.replace(" ", "").lower()
      if User.objects.filter(email=customer.email).exists():
        print("Usuario já existe...") 
        user = User.objects.filter(email=customer.email)
      else:
        user = User.objects.create_user(usuarioo, customer.email, password)
        user.save()
        criado_usuario = True

      customer.user = user
      customer.save()
        
    except:
      user = User.objects.filter(email=customer.email)
      customer.user = user
      customer.save()
      print('Usuario já existe...')

  total = float(data['form']['total'].replace(",", "."))
  order.transaction_id = transaction_id

  #print("<<<<<<<<<<<<<<<", total)
  #print("<<<<<<<<<<<<<<<", order.get_cart_total)
  
  if total == order.get_cart_total: 
    order.complete = True 
    order.status = "pago"
  order.save()
  
  if order.shipping == True:
    # aqui deveriamos verificar se já existe este envio!! pelo pedido numero ?
    ShippingAddress.objects.create(
    	customer=customer,
    	order=order,
    	address=data['shipping']['address'],
    	city=data['shipping']['city'],
    	state=data['shipping']['state'],
    	zipcode=data['shipping']['zipcode'],
    	)

  # aqui poderá ir um email para o customer informando da compra!
  try:
    send_mail(subject='Compra na Nipponime',
           message=newOrderMsg(customer, data),
           from_email=settings.EMAIL_HOST_USER,
           recipient_list=[customer.email])
  except Exception as e:
    print("Erro enviar email 156", e)
  
  if criado_usuario:
    try:
      send_mail(subject='Usuario na Nipponime',
           message=newGestUserMsg(customer, usuarioo, password),
           from_email=settings.EMAIL_HOST_USER,
           recipient_list=[customer.email])
    except Exception as e:
      print("Erro enviar email 165", e)

  #email para mim para saber sobre a compra
  try:
    send_mail(subject='Compra na Nipponime',
            message='\n' + str(customer.name) +  '.\n pedidoID: ' + str(order.id) + '\n clienteID: ' + str(customer.id) + '\nTotal: ' + str(order.get_cart_total) +  '\n\nStaff,\nNIPPONIME 2023',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER])
  except Exception as e:
      print("Erro enviar email 174", e)
  

  return JsonResponse('Payment submitted..', safe=False)
  
def register_request(request):
  if request.method == "POST":
    form = NewUserForm(request.POST)
    
    if form.is_valid():
      user = form.save()
      customer, criado = Customer.objects.get_or_create(email=user.email)
      customer.name = user.first_name + " " + user.last_name
      customer.user = user
      customer.save()
      # fazemos o login já como esta nova conta
      login(request, user)
      # Vamos enviar uma mensagem a esta nova conta!
      
      msg = Msg(who="Nipponime", customer=customer, title="Registro" , message=welcomeMsg(user))
      msg.save()
     
      try:
        send_mail(subject='Usuario na Nipponime', message=welcomeMsg(user),
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[customer.email])
      except Exception as e:
        print("Erro enviar email ", e)

      messages.success(request, "Registro bem-sucedido." )
      return redirect("/")
    messages.error(request, form.errors)
  form = NewUserForm()
  return render (request=request, template_name="store/Register.html", context={"register_form":form})
  
def details(request, slug):
 
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  product = Product.objects.get(slug=slug)
  products = Product.objects.filter(title=product.title).exclude(id=product.id).order_by('-id')
  category = Category.objects.all()

  
  groups = []
  index = 0
  
  for j in range(math.ceil((products.count()) / 4)):
    group = []
    for x in range(4):
      if index > products.count() - 1:
        break
      group.append(products[index])
    
      if x == 3 or index == products.count() - 1:
        groups.append(group)
      index +=1

  print("groups: ", groups)
  context = {'product':product, 'cartItems':cartItems, 'products':products, 'category':category, 'groups':groups}
  return render(request, 'store/Details.html', context)
  
def profile(request, id):
  
  customer = request.user.customer
  
  if request.method == "POST":
    form = ClientForm(request.POST, instance=customer)
    if form.is_valid():
      form.save()
      return redirect('/perfil/' + str(customer.id))
  else:
    form = ClientForm(instance=customer)
    
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  Products = Product.objects.all()  
  #orders = Order.objects.filter(customer=customer, complete=True)
  shippingaddress = ShippingAddress.objects.filter(customer=customer).order_by('-id')
  mensagens = Msg.objects.filter(customer=customer)
  
  context = {'Products':Products, 'cartItems':cartItems, 'customer':customer, 'shippingaddress':shippingaddress, 'mensagens':mensagens, 'form':form}  

  return render(request, 'store/Profile.html', context)
  
def client(request, id):
  
  client = Customer.objects.get(id=id)
  
  if request.method == "POST":
    form = ClientForm(request.POST, instance=client)
    if form.is_valid():
      form.save()
      return redirect('/perfil/')
  else:
    form = ClientForm(instance=client)
    
  return render(request, "store/Client.html", {"form": form})
  
def updateFavs(request):
  if (request.body):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    if action == 'add':
      customer.favorites.add(Product.objects.get(id=productId))
      customer.save()
    elif action == 'remove':
      customer.favorites.remove(Product.objects.get(id=productId))
    customer.save()
  
  return JsonResponse('Produto foi adicionado', safe=False)
  
def arquivarmsg(request):
  if (request.body):
    data = json.loads(request.body)
    id = data['id']
    customer = request.user.customer
    msg = Msg.objects.filter(customer=customer, id=id)
    if msg != None and msg[0] != None :
      Msg.objects.filter(id=id).update(archive=True)
      print("mensagem arquivada?: ", msg[0].archive)
  return JsonResponse('Mensagem arquivada', safe=False)
  
def contact(request):
  
  if request.user.is_authenticated: 
    customer = request.user.customer
  else:
    customer = {}
    
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items'] 
  
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      subject = "NIPPONIME CONTACTO"
      body = {
  			'nome': form.cleaned_data['Name'], 
  			'email': form.cleaned_data['Email'], 
  			'mensagem':form.cleaned_data['Message'], 
  			}
      message = "\n".join(body.values())
      print(message)
      try:
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.EMAIL_HOST_USER])
      except BadHeaderError:
        return HttpResponse('Invalid header found.')
      return redirect ("/")  
    else:
      print("validação do formulario com erros")
  else:         
    form = ContactForm()
  
  context = {'items':items, 'order':order, 'cartItems':cartItems, 'form':form, 'customer':customer}
  return render(request, 'store/Contact.html', context)
  
def search(request):
  if request.user.is_authenticated: 
    customer = request.user.customer
  else:
    customer = {}
    
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  category = Category.objects.all()

  search_post = request.GET.get('search')
  if search_post:
    # vai juntar a procura nos titulos, icontains procura seja por minusculas ou maiusculas
    products = Product.objects.filter(name__contains=search_post).order_by('tag').order_by('-is_promo')
    if (products.count() == 0):
      # em caso de não achar nenhum produto, para não dar erro na paginação! crio uma tuple vazia
      products = tuple()
  else:
    products = tuple()
  
  paginator = Paginator(products, 6) # Mostrar 6 produtos por página.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context={'cartItems':cartItems, 'category':category, 'customer':customer, 'page_obj':page_obj, 'name':search_post}
  
  return render(request, "store/Search.html", context)

def mangasdetalhes(request, slug):
  if request.user.is_authenticated: 
    cliente = request.user.customer
  else:
    cliente = {}
    
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  
  if (slug.upper() == "ALL"):
    products = Product.objects.all()
    
  if (slug.upper() == 'PROMO'):
    products = Product.objects.filter(is_promo=True).order_by('-tag')

  if (slug.upper() != 'ALL' and slug.upper() != 'PROMO' ): 
    products = Product.objects.filter(Q(main_category__slug__contains=slug) | Q(sub_category__slug__contains=slug)).distinct()
    
  category = Category.objects.all().order_by('name')
  paginator = Paginator(products, 12) # Mostrar 12 produtos por página.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {'page_obj':page_obj, 'cartItems':cartItems, 'category':category, 'customer':cliente}
  
  return render(request, 'store/Mangas.html', context)


