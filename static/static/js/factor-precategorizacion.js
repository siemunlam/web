	loadFactoresPC(fdpc_records, fdpc_api_url)
	$('.nav-tabs a[href="#reglas-fdpc"]').on('show.bs.tab', event => {
		loadFactoresPC(fdpc_records, fdpc_api_url)
	})

	function loadFactoresPC(dest, apiURL) {
		dest.innerHTML = ''
		
		fetch(apiURL, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response)
		}).then(response => {
			return response.json()
		}).then(jsonData => {
			jsonData.results.map((factorpc) => {
				let newRow = dest.insertRow(dest.rows.length)
				const acciones = `
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorPCDetailModal" title='Detalle'>
						<span class="glyphicon glyphicon-list" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorPCUpdateModal" title='Editar'>
						<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorPCDeleteModal" title='Eliminar'>
						<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
					</button>`
				newRow.innerHTML = `<td class='font-bold'>${factorpc.id}</td>
									<td>${factorpc.descripcion}</td>
									<td>${acciones}</td>`
			})
			setPaginationInfo(jsonData.previous, jsonData.next, jsonData.results.length, jsonData.count)
		}).catch(error => {
			console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
		})
    }
    

    function setPaginationInfo(previous, next, currentAmount, totalAmount) {
		document.getElementById('CurrentPageAmount').innerText = currentAmount
		document.getElementById('TotalAmount').innerText = totalAmount

		if(previous === null)
			document.querySelector('#fdpcPager > .previous').classList.add('disabled')
		else {
			document.querySelector('#fdpcPager > .previous').classList.remove('disabled')
			document.querySelector('#fdpcPager > .previous > a').link = previous
		}
		if(next === null)
			document.querySelector('#fdpcPager > .next').classList.add('disabled')
		else {
			document.querySelector('#fdpcPager > .next').classList.remove('disabled')
			document.querySelector('#fdpcPager > .next > a').link = next
		}
    }
    

	/*
	 * AddFactorPCModal Layout
	 */
	const divs_create_FactorPC = document.getElementById('AddFactorPCForm').getElementsByTagName('div')
	divs_create_FactorPC[0].classList.add('col-md-12')

	/*
	 * CreateFactorPC
	 */
	document.getElementById('AddFactorPCForm').onsubmit = function createFactorPC(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('AddFactorPCForm')),
			credentials: 'same-origin'
		}

		fetch(fdpc_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El factor de precategorización \"${jsonData.descripcion}\" fue registrada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddFactorPCForm').reset()

					$('#AddFactorPCModal').modal('hide')
					loadFactoresPC(fdpc_records, fdpc_api_url)
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
	 * UpdateFactorPCModal Layout
	 */
	const divs_update_FactorPC = document.getElementById('UpdateFactorPCForm').getElementsByTagName('div')
	divs_update_FactorPC[0].classList.add('col-md-12')


	/*
	 * UpdateFactorPC
	 */
	 document.getElementById('UpdateFactorPCForm').onsubmit = function createFactorPC(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('UpdateFactorPCForm')),
			credentials: 'same-origin'
		}

		const FactorPCId = document.getElementById('FactorPCUpdateModalId').innerText;

		fetch(`${fdpc_api_url}${FactorPCId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">El factor de precategorización \"${jsonData.descripcion}\" fue actualizado
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateFactorPCForm').reset()

					$('#FactorPCUpdateModal').modal('hide')
					loadFactoresPC(fdpc_records, fdpc_api_url)
					
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
	 * FactorPCUpdateModal Handler
	 */
	 $('#FactorPCUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const factorPCId = clickedButton.closest('tr').find('td:eq(0)').text();

		fetch(`${fdpc_api_url}${factorPCId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateFactorPCForm > div > input[name="descripcion"]').value = jsonData.descripcion;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle del factor de precategorización Id ${factorPCId}: ${error.message}`);
		});
		document.getElementById('FactorPCUpdateModalId').innerText = factorPCId;
	});
	

	document.getElementById('DeleteFactorPCForm').onsubmit = function deleteFactorPC(event) {
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
		
		const factorPCId = document.getElementById('FactorPCDeleteModalId').innerText;

		fetch(`${fdpc_api_url}${factorPCId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">Factor de precategorización con Id: ${factorPCId} fue eliminado
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				loadFactoresPC(fdpc_records, fdpc_api_url);
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
		$('#FactorPCDeleteModal').modal('hide');
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * FactorPCDeleteModal Handler
	 */
	 $('#FactorPCDeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const FactorPCId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('FactorPCDeleteModalId').innerText = FactorPCId;
	});
