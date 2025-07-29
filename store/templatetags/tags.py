from django import template
from store.models import * 

register = template.Library()

@register.filter(name='is_Favorite')
def is_Favorite(customer, product):
  resultado = Customer.objects.filter(pk=customer.pk, favorites__pk=product).exists()
  #print(">>>>> result: " , resultado)  
  return resultado

@register.filter(name='times') 
def times(number):
    return range(number)