from django.urls import path, include
from . import views

urlpatterns = [
        #Deixe como string vazia para url base
	path('', views.store, name="store"),
	path('carrinho/', views.cart, name="cart"),
	path('finalizar/', views.checkout, name="checkout"),
  path('update_item/', views.updateItem, name="update_item"),
  path('process_order/', views.processOrder, name="process_order"),
  path("accounts/", include("django.contrib.auth.urls")),
  path("register", views.register_request, name="register"),
  path('detalhes/<slug:slug>/', views.details, name='details'),
  path('perfil/<int:id>/', views.profile, name='profile'),
  path('cliente/<int:id>/', views.client, name='client'),
  path('update_fav/', views.updateFavs, name="update_fav"),
  path('mensagens/', views.arquivarmsg, name="arquivar"),
  path('contacto/', views.contact, name='contact'),
  path('procura/', views.search, name="procura"),
  path('mangas/<slug:slug>/', views.mangasdetalhes, name='mangas'),
]