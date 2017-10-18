	/*
	 * AddValorFactorAModal Layout
	 */
	const divs_create_ValorFactorA = document.getElementById('AddValorFactorAForm').getElementsByTagName('div')
	divs_create_ValorFactorA[0].classList.add('col-md-12')
	divs_create_ValorFactorA[1].style = 'display:none;'

	/*
	 * CreateValorFactorA
	 */
	document.getElementById('AddValorFactorAForm').onsubmit = function createValorFactorA(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}
		
		var formData = new FormData(document.getElementById('AddValorFactorAForm'));
		const FactorAId = document.getElementById('ValorFactorAAddModalId').innerText;
		formData.append("factorDeAjuste", FactorAId);

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: formData,
			credentials: 'same-origin'
		}

		fetch(vdfda_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El valor \"${jsonData.descripcion}\" del factor de ajuste fue registrado
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddValorFactorAForm').reset()

					$('#AddValorFactorAModal').modal('hide')
					// loadFactoresA(fda_records, vdfda_api_url)
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
		event.preventDefault()	// Evita el envío POST del botón
		window.scrollTo(0,0)	// Scroll a la parte superior de la pantalla
	}


	/*
	 * UpdateValorFactorAModal Layout
	 */
	const divs_update_ValorFactorA = document.getElementById('UpdateValorFactorAForm').getElementsByTagName('div')
	divs_update_ValorFactorA[0].classList.add('col-md-12')

	/*
	 * UpdateValorFactorA
	 */
	 document.getElementById('UpdateValorFactorAForm').onsubmit = function createValorFactorA(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		var formData = new FormData(document.getElementById('UpdateValorFactorAForm'));
		const FactorAId = document.getElementById('ValorFactorAUpdateModalFactorId').innerText;
		formData.append("factorDeAjuste", FactorAId);
		const ValorFactorAId = document.getElementById('ValorFactorAUpdateModalId').innerText;		

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: formData,
			credentials: 'same-origin'
		}

		fetch(`${vdfda_api_url}${ValorFactorAId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El valor \"${jsonData.descripcion}\" del factor de ajuste fue actualizado
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateValorFactorAForm').reset()

					$('#ValorFactorAUpdateModal').modal('hide')
					// loadFactoresA(fda_records, vdfda_api_url)
					
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
		event.preventDefault()	// Evita el envío POST del botón
		window.scrollTo(0,0)	// Scroll a la parte superior de la pantalla
	}	


	/*
	 * ValorFactorAUpdateModal Handler
	 */
	 $('#ValorFactorAUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const valorFactorAId = clickedButton.closest('tr').find('td:eq(0)').text();
		const factorDeAjusteId = clickedButton.closest('tr').find('td:eq(2)').text();
		fetch(`${vdfda_api_url}${valorFactorAId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateValorFactorAForm > div > input[name="descripcion"]').value = jsonData.descripcion;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle del valor del factor de ajuste Id ${valorFactorAId}: ${error.message}`);
		});
		document.getElementById('ValorFactorAUpdateModalId').innerText = valorFactorAId;
		document.getElementById('ValorFactorAUpdateModalFactorId').innerText = factorDeAjusteId;
	});
	

	document.getElementById('DeleteValorFactorAForm').onsubmit = function deleteValorFactorA(event) {
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
		
		const ValorFactorAId = document.getElementById('ValorFactorADeleteModalId').innerText;

		fetch(`${vdfda_api_url}${ValorFactorAId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">El valor del factor de ajuste con Id: ${ValorFactorAId} fue eliminado
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				// loadFactoresA(fda_records, vdfda_api_url);
			} else {
				response.json()
				.then(jsonData => {
					Object.keys(jsonData).map(key => {
						// Mostrar mensaje de error
						document.querySelector('.messages').innerHTML += `
						<div class="alert alert-dismissable fade in alert-danger">${key}: ${jsonData[key]}
							<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
						</div>`;
					});
				});
			}
		});
		$('#ValorFactorADeleteModal').modal('hide');
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * ValorFactorADeleteModal Handler
	 */
	 $('#ValorFactorADeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const ValorFactorAId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('ValorFactorADeleteModalId').innerText = ValorFactorAId;
	});
