	loadReglasA(rda_records, rda_api_url)
	$('.nav-tabs a[href="#reglas-rda"]').on('show.bs.tab', event => {
		loadReglasA(rda_records, rda_api_url)
	})

	function loadReglasA(dest, apiURL) {
		dest.innerHTML = ''
		
		fetch(apiURL, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response)
		}).then(response => {
			return response.json()
		}).then(jsonData => {
			jsonData.map((regla_a) => {
				let newRow = dest.insertRow(dest.rows.length)
				const acciones = `
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ReglaAUpdateModal" title='Editar'>
						<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ReglaADeleteModal" title='Eliminar'>
						<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
					</button>`
				newRow.innerHTML = `<td class='font-bold'>${regla_a.id}</td>
									<td style="display:none;">${regla_a.condicion}</td>
									<td>${regla_a.condicion_factora_descripcion} es ${regla_a.condicion_descripcion}</td>
									<td style="display:none;">${regla_a.resultado}</td>
									<td>${regla_a.resultado_valor}</td>
									<td>${regla_a.prioridad}</td>
									<td>${acciones}</td>`
			})
			if (dest.innerHTML == '') {
				let newRow = dest.insertRow(dest.rows.length)
				newRow.innerHTML = `<td class="text-center" id='blank_row' bgcolor="#FFFFFF" colspan="3">Ninguna regla de ajuste creada</td>`
			}
		}).catch(error => {
			console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
		})
    }
    

	/*
	 * AddReglaAModal Layout
	 */
	const divs_create_ReglaA = document.getElementById('AddReglaAForm').getElementsByTagName('div')
	divs_create_ReglaA[0].classList.add('col-md-12')
	divs_create_ReglaA[1].classList.add('col-md-6')
	divs_create_ReglaA[2].classList.add('col-md-6')
	/*
	 * CreateReglaA
	 */
	document.getElementById('AddReglaAForm').onsubmit = function createReglaA(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('AddReglaAForm')),
			credentials: 'same-origin'
		}

		fetch(rda_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La regla de ajuste \"${jsonData.condicion}\" fue registrada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddReglaAForm').reset()

					$('#AddReglaAModal').modal('hide')
					loadReglasA(rda_records, rda_api_url)
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
	 * UpdateReglaAModal Layout
	 */
	const divs_update_ReglaA = document.getElementById('UpdateReglaAForm').getElementsByTagName('div')
	divs_update_ReglaA[0].classList.add('col-md-12')
	divs_update_ReglaA[1].classList.add('col-md-6')
	divs_update_ReglaA[2].classList.add('col-md-6')

	/*
	 * UpdateReglaA
	 */
	 document.getElementById('UpdateReglaAForm').onsubmit = function createReglaA(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('UpdateReglaAForm')),
			credentials: 'same-origin'
		}

		const ReglaAId = document.getElementById('ReglaAUpdateModalId').innerText;

		fetch(`${rda_api_url}${ReglaAId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La regla de ajuste \"${jsonData.condicion}\" fue actualizada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateReglaAForm').reset()

					$('#ReglaAUpdateModal').modal('hide')
					loadReglasA(rda_records, rda_api_url)
					
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
	 * ReglaAUpdateModal Handler
	 */
	 $('#ReglaAUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const reglaAId = clickedButton.closest('tr').find('td:eq(0)').text();
		fetch(`${rda_api_url}${reglaAId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateReglaAForm > div > select[name="condicion"]').value = jsonData.condicion;
			document.querySelector('#UpdateReglaAForm > div > select[name="resultado"]').value = jsonData.resultado;
			document.querySelector('#UpdateReglaAForm > div > input[name="prioridad"]').value = jsonData.prioridad;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle de la regla de ajuste Id ${reglaAId}: ${error.message}`);
		});
		document.getElementById('ReglaAUpdateModalId').innerText = reglaAId;
	});
	

	document.getElementById('DeleteReglaAForm').onsubmit = function deleteReglaA(event) {
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
		
		const reglaAId = document.getElementById('ReglaADeleteModalId').innerText;

		fetch(`${rda_api_url}${reglaAId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">La regla de ajuste con Id: ${reglaAId} fue eliminada
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				loadReglasA(rda_records, rda_api_url);
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
		$('#ReglaADeleteModal').modal('hide');
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * ReglaADeleteModal Handler
	 */
	 $('#ReglaADeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const ReglaAId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('ReglaADeleteModalId').innerText = ReglaAId;
	});
