var updateButtons = document.getElementsByClassName('adicionar-ao-carrinho')

for (var i = 0; i< updateButtons.length; i++){
    updateButtons[i].addEventListener('click',function()
    {
        var vinhoId= this.dataset.wine
        var acao = this.dataset.acao
        console.log('ID', vinhoId)
        console.log('USER', user)
        if(user ==='AnonymousUser'){
            console.log("ANONIMO")
        }else{
			atualizarPedido(vinhoId, acao)
		}
    })
}

function atualizarPedido(vinhoId, acao){
    var url = '/adegadobairro/update_item/'

    fetch(url, {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'vinhoid':vinhoId, 'acao':acao})
            })
            .then((response) => {
               return response.json();
            })
            .then((data) => {
                location.reload()
            });
}

function addCookieItem(vinhoId, acao){
	console.log('User is not authenticated')

	if (acao == 'add'){
		if (pedido_vinho[vinhoId] == undefined){
		pedido_vinho[vinhoId] = {'quantidade':1}

		}else{
			pedido_vinho[vinhoId]['quantidade'] += 1
		}
	}

	if (action == 'remove'){
		pedido_vinho[vinhoId]['quantidade'] -= 1

		if (pedido_vinho[vinhoId]['quantidade'] <= 0){
			console.log('Apagar Vinho')
			delete pedido_vinho[vinhoId];
		}
	}
	console.log('pedido_vinho:', pedido_vinho)
	document.cookie ='pedido_vinho=' + JSON.stringify(pedido_vinho) + ";domain=;path=/"

	location.reload()
}