from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Category(models.Model):
  name = models.CharField(max_length=200)
  slug = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name
    
class Tag(models.Model):
  name = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name
    
class BackgroundImage(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(null=True, blank=True)

  def __str__(self):
    return self.name    
    
class Product(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField()
  description = models.TextField(blank=True, null=True)
  is_promo = models.BooleanField(default = False)
  price_promo = models.FloatField()
  image = models.ImageField(null=True, blank=True)
  pages = models.CharField(max_length=200, null=True, blank=True)
  format = models.CharField(max_length=200, null=True, blank=True)
  ean = models.CharField(max_length=200, null=True, blank=True)
  author = models.CharField(max_length=200, null=True, blank=True)
  main_category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
  sub_category = models.ManyToManyField(Category, related_name="subcategory")
  tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
  slug = models.SlugField(null=True, unique=True)
  title = models.CharField(max_length=200)
  promo_start_date = models.DateField(null=True, blank=True)
  promo_end_date = models.DateField(null=True, blank=True)
  backgroundimage = models.ForeignKey(BackgroundImage, on_delete=models.SET_NULL, null=True)
  
  
  def __str__(self):
    return self.name

  @property
  def IsPromo(self):
    today = date.today()
    if(self.is_promo == True):
      if(self.promo_start_date and self.promo_end_date ):
        if (today >= self.promo_start_date and today <= self.promo_end_date):
          return True
        else:
          return False
      else:
        return False
    else:
      return False 
    
  @property
  def getPrice(self):
    today = date.today()
    if(self.is_promo == True):
      if(self.promo_start_date and self.promo_end_date ):
        if (today >= self.promo_start_date and today <= self.promo_end_date):
          return float("{:.2f}".format(self.price_promo))
        else:
          return float("{:.2f}".format(self.price))
      else:
        return float("{:.2f}".format(self.price))
    else:
      return float("{:.2f}".format(self.price))
      
  @property
  def imageURL(self):
    #print(self.image.url)
    try:
      url = self.image.url
    except:
      url = ''
    return url

  @property
  def imagebkURL(self):
    #print(self.backgroundimage.image.url)
    try:
      url1 = self.backgroundimage.image.url
    except:
      url1 = ''
    return url1
    
class Customer(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, blank=True)
  email = models.CharField(max_length=200)
  nif = models.CharField("NIF", max_length=200, null=True, blank=True)
  favorites = models.ManyToManyField(Product, related_name='favorites', blank=True)
  def __str__(self):
    return self.name
    
class Order(models.Model):
  STATUS = (
    ("pendente", "Pendente"),
    ("pago", "Pago"),
    ("enviado", "Enviado"),
    ("recebido", "Recebido"),
)
  
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False)
  transaction_id = models.CharField(max_length=100, null=True)
  status = models.CharField(max_length=50, choices=STATUS, blank=False, default="pendente")
  invoice = models.FileField(upload_to="faturas/", null=True, blank=True)
  
  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return float("{:.2f}".format(total))
  
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total

  @property
  def shipping(self):
    # se no futuro tiver produtos digitais que nao precisam de enviar fisicamente
    '''
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
		  if i.product.digital == False:
			 shipping = True
    '''
    return True
  
  def __str__(self):
    return str(self.id)
    
class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total
  
  def __str__(self): 
    return str(self.id)
    
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
    
class Msg(models.Model):
  who = models.CharField(max_length=200, default='Nipponime')
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  title = models.CharField(max_length=200, null=False)
  message = models.TextField(null=False)
  date_added = models.DateTimeField(auto_now_add=True)
  archive = models.BooleanField(default=False)
  def __str__(self):
    return str(self.title)

  