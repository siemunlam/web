	loadReglasPC(rdpc_records, rdpc_api_url)
	$('.nav-tabs a[href="#reglas-rdpc"]').on('show.bs.tab', event => {
		loadReglasPC(rdpc_records, rdpc_api_url)
	})

	function loadReglasPC(dest, apiURL) {
		dest.innerHTML = ''
		
		fetch(apiURL, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response)
		}).then(response => {
			return response.json()
		}).then(jsonData => {
			jsonData.map((reglapc) => {
				let newRow = dest.insertRow(dest.rows.length)
				const acciones = `
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ReglaPCUpdateModal" title='Editar'>
						<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ReglaPCDeleteModal" title='Eliminar'>
						<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
					</button>`
				newRow.innerHTML = `<td class='font-bold'>${reglapc.id}</td>
									<td style="display:none;">${reglapc.condicion}</td>
									<td>${reglapc.condicion_factorpc_descripcion} es ${reglapc.condicion_descripcion}</td>
									<td style="display:none;">${reglapc.resultado}</td>
									<td>${reglapc.resultado_descripcion}</td>
									<td>${reglapc.prioridad}</td>
									<td>${acciones}</td>`
			})
			if (dest.innerHTML == '') {
				let newRow = dest.insertRow(dest.rows.length)
				newRow.innerHTML = `<td class="text-center" id='blank_row' bgcolor="#FFFFFF" colspan="3">Ninguna regla de precategorización creada</td>`
			}
		}).catch(error => {
			console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
		})
    }
    

	/*
	 * AddReglaPCModal Layout
	 */
	const divs_create_ReglaPC = document.getElementById('AddReglaPCForm').getElementsByTagName('div')
	divs_create_ReglaPC[0].classList.add('col-md-12')
	divs_create_ReglaPC[1].classList.add('col-md-6')
	divs_create_ReglaPC[2].classList.add('col-md-6')
	/*
	 * CreateReglaPC
	 */
	document.getElementById('AddReglaPCForm').onsubmit = function createReglaPC(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('AddReglaPCForm')),
			credentials: 'same-origin'
		}

		fetch(rdpc_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La regla de precategorización \"${jsonData.condicion}\" fue registrada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddReglaPCForm').reset()

					$('#AddReglaPCModal').modal('hide')
					loadReglasPC(rdpc_records, rdpc_api_url)
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
	 * UpdateReglaPCModal Layout
	 */
	const divs_update_ReglaPC = document.getElementById('UpdateReglaPCForm').getElementsByTagName('div')
	divs_update_ReglaPC[0].classList.add('col-md-12')
	divs_update_ReglaPC[1].classList.add('col-md-6')
	divs_update_ReglaPC[2].classList.add('col-md-6')

	/*
	 * UpdateReglaPC
	 */
	 document.getElementById('UpdateReglaPCForm').onsubmit = function createReglaPC(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('UpdateReglaPCForm')),
			credentials: 'same-origin'
		}

		const ReglaPCId = document.getElementById('ReglaPCUpdateModalId').innerText;

		fetch(`${rdpc_api_url}${ReglaPCId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La regla de precategorización \"${jsonData.condicion}\" fue actualizada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateReglaPCForm').reset()

					$('#ReglaPCUpdateModal').modal('hide')
					loadReglasPC(rdpc_records, rdpc_api_url)
					
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
	 * ReglaPCUpdateModal Handler
	 */
	 $('#ReglaPCUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const reglaPCId = clickedButton.closest('tr').find('td:eq(0)').text();
		console.log("obtuvo: " + reglaPCId);
		fetch(`${rdpc_api_url}${reglaPCId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateReglaPCForm > div > select[name="condicion"]').value = jsonData.condicion;
			document.querySelector('#UpdateReglaPCForm > div > select[name="resultado"]').value = jsonData.resultado;
			document.querySelector('#UpdateReglaPCForm > div > input[name="prioridad"]').value = jsonData.prioridad;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle de la regla de precategorización Id ${reglaPCId}: ${error.message}`);
		});
		document.getElementById('ReglaPCUpdateModalId').innerText = reglaPCId;
	});
	

	document.getElementById('DeleteReglaPCForm').onsubmit = function deleteReglaPC(event) {
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
		
		const reglaPCId = document.getElementById('ReglaPCDeleteModalId').innerText;

		fetch(`${rdpc_api_url}${reglaPCId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">La regla de precategorización con Id: ${reglaPCId} fue eliminada
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				loadReglasPC(rdpc_records, rdpc_api_url);
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
		$('#ReglaPCDeleteModal').modal('hide');
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * ReglaPCDeleteModal Handler
	 */
	 $('#ReglaPCDeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const ReglaPCId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('ReglaPCDeleteModalId').innerText = ReglaPCId;
	});
