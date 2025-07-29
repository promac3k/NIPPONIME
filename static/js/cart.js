//console.log("cart.js eu sou gustavo")

var updateBtns = document.getElementsByClassName('update-cart')
var updateBtns2 = document.getElementsByClassName('delete-allitems')
var updateFavs = document.getElementsByClassName('update-favs')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
    console.log('USER:', user)
    
    var qt = document.getElementById('QT' + productId)
    if (qt == null){
      qt = 1
    }
    else {
      qt = parseInt(qt.value)
    }
    console.log('QT:', qt)
    
    if (user == 'AnonymousUser'){
    	addCookieItem(productId, action, qt)
    			
    }else{
      updateUserOrder(productId,action, qt)
    }
	})
}

for (i = 0; i < updateBtns2.length; i++) {
	updateBtns2[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
    var quantity = this.dataset.quantity
		//console.log('productId:', productId, 'Action:', action , 'quantity:', quantity)
    //console.log('user:', user)
    if (user == 'AnonymousUser'){    	  	
      addCookieItem(productId, action, quantity)
    }else{
      updateUserOrder(productId, action, quantity)
    }
    	})
}

for (i = 0; i < updateFavs.length; i++) {
	updateFavs[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
    var cliente = this.dataset.cliente
		//console.log('productId:', productId, 'Action:', action , 'cliente:', cliente)
    //console.log('user:', user)
    if (user == 'AnonymousUser'){    	  	
      alert("Usuario não existe");
    }else{
      updateFavoritos(productId, action, cliente)
    }
    	})
}

function updateUserOrder(productId, action, qt){
	  console.log('O usuário está autenticado, enviando dados...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'quant': qt})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});

}

function addCookieItem(productId, action, qt){
  console.log('O usuário não está autenticado')
    
    	if (action == 'add'){
    		if (cart[productId] == undefined){
    		cart[productId] = {'quantity':qt}
    
    		}else{
    			cart[productId]['quantity'] += qt
    		}
    	}

      if (action == 'remove'){
      		cart[productId]['quantity'] -= qt
      
      		if (cart[productId]['quantity'] <= 0){
      			console.log('O item deve ser excluído')
      			delete cart[productId];
      		}
      }
      	console.log('CART:', cart)
      	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
  
      	location.reload()
}

function updateFavoritos(productId, action){
  //console.log('updateFavoritos, sending data...')  
  //console.log("productId: " + productId)
  //console.log("action: " + action)
  const url = window.location.href;
  
  fetch('/update_fav/', {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		}).then((response) => {
		   return response.json();
		}).then((data) => {
      if (url.includes('perfil') ){
        location.reload()
      } else {
        var favicon =  document.getElementById("fav" + productId);
        if (action == "add"){
          favicon.innerHTML = '<ion-icon style="color:red" name="heart-sharp" size="small" role="img" class="md icon-small hydrated" aria-label="heart sharp"></ion-icon>';
          favicon.setAttribute("data-action", "remove");
        }
        if (action == "remove"){
          favicon.innerHTML = '<ion-icon name="heart-outline" size="small" role="img" class="md icon-small hydrated" aria-label="heart sharp"></ion-icon>';
          favicon.setAttribute("data-action", "add");
        }
        
      }
    
		});
  
}
