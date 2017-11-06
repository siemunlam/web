	/*
	 * AddValorFactorPCModal Layout
	 */
	const divs_create_ValorFactorPC = document.getElementById('AddValorFactorPCForm').getElementsByTagName('div')
	divs_create_ValorFactorPC[0].classList.add('col-md-12')
	divs_create_ValorFactorPC[1].style = 'display:none;'

	/*
	 * CreateValorFactorPC
	 */
	document.getElementById('AddValorFactorPCForm').onsubmit = function createValorFactorPC(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}
		
		var formData = new FormData(document.getElementById('AddValorFactorPCForm'));
		const FactorPCId = document.getElementById('ValorFactorPCAddModalId').innerText;
		formData.append("factorDePreCategorizacion", FactorPCId);

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: formData,
			credentials: 'same-origin'
		}

		fetch(vdfdpc_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El valor \"${jsonData.descripcion}\" del factor de precategorización fue registrado
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddValorFactorPCForm').reset()
					loadValoresFactorPC();
				} else {
					Object.keys(jsonData).map(key => {
						// Mostrar mensaje de error
						document.querySelector('.messages').innerHTML += `
						<div class="alert alert-dismissable fade in alert-danger">${key}: ${jsonData[key]}
							<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
						</div>`;
					})
				}
			})
		})
		$('#AddValorFactorPCModal').modal('hide')
		event.preventDefault()	// Evita el envío POST del botón
		window.scrollTo(0,0)	// Scroll a la parte superior de la pantalla
	}


	/*
	 * UpdateValorFactorPCModal Layout
	 */
	const divs_update_ValorFactorPC = document.getElementById('UpdateValorFactorPCForm').getElementsByTagName('div')
	divs_update_ValorFactorPC[0].classList.add('col-md-12')

	/*
	 * UpdateValorFactorPC
	 */
	 document.getElementById('UpdateValorFactorPCForm').onsubmit = function createValorFactorPC(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		var formData = new FormData(document.getElementById('UpdateValorFactorPCForm'));
		const FactorPCId = document.getElementById('ValorFactorPCUpdateModalFactorId').innerText;
		formData.append("factorDePreCategorizacion", FactorPCId);
		const ValorFactorPCId = document.getElementById('ValorFactorPCUpdateModalId').innerText;		

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: formData,
			credentials: 'same-origin'
		}

		fetch(`${vdfdpc_api_url}${ValorFactorPCId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El valor \"${jsonData.descripcion}\" del factor de precategorización fue actualizado
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateValorFactorPCForm').reset()
					loadValoresFactorPC();				
				} else {
					Object.keys(jsonData).map(key => {
						// Mostrar mensaje de error
						document.querySelector('.messages').innerHTML += `
						<div class="alert alert-dismissable fade in alert-danger">${key}: ${jsonData[key]}
							<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
						</div>`;
					})
				}
			})
		})
		$('#ValorFactorPCUpdateModal').modal('hide')
		event.preventDefault()	// Evita el envío POST del botón
		window.scrollTo(0,0)	// Scroll a la parte superior de la pantalla
	}	


	/*
	 * ValorFactorPCUpdateModal Handler
	 */
	 $('#ValorFactorPCUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const valorFactorPCId = clickedButton.closest('tr').find('td:eq(0)').text();
		const factorDePreCategorizacionId = clickedButton.closest('tr').find('td:eq(2)').text();
		fetch(`${vdfdpc_api_url}${valorFactorPCId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateValorFactorPCForm > div > input[name="descripcion"]').value = jsonData.descripcion;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle del valor del factor de precategorización Id ${valorFactorPCId}: ${error.message}`);
		});
		document.getElementById('ValorFactorPCUpdateModalId').innerText = valorFactorPCId;
		document.getElementById('ValorFactorPCUpdateModalFactorId').innerText = factorDePreCategorizacionId;
	});
	

	document.getElementById('DeleteValorFactorPCForm').onsubmit = function deleteValorFactorPC(event) {
		document.querySelector('.messages').innerHTML = '';

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'DELETE',
			headers: new Headers(header_init),
			credentials: 'same-origin'
		};
		
		const ValorFactorPCId = document.getElementById('ValorFactorPCDeleteModalId').innerText;

		fetch(`${vdfdpc_api_url}${ValorFactorPCId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">El valor del factor de precategorización Nro: ${ValorFactorPCId} fue eliminado
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				loadValoresFactorPC();
			} else {
				response.json()
				.then(jsonData => {
					// Mostrar mensaje de error
					document.querySelector('.messages').innerHTML += `
					<div class="alert alert-dismissable fade in alert-danger">${jsonData}
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`;
				});
			}
		});
		$('#ValorFactorPCDeleteModal').modal('hide');
		$('#FactorPCDetailModal').modal('hide')
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * ValorFactorPCDeleteModal Handler
	 */
	 $('#ValorFactorPCDeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const ValorFactorPCId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('ValorFactorPCDeleteModalId').innerText = ValorFactorPCId;
	});
