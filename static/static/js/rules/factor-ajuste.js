loadFactoresA(fda_records, fda_api_url)
$('.nav-tabs a[href="#reglas-fda"]').on('show.bs.tab', event => {
	loadFactoresA(fda_records, fda_api_url)
})

function loadFactoresA(dest, apiURL) {
	dest.innerHTML = ''
	
	fetch(apiURL, getAuthorizedFetchOption()).then(response => {
		return checkStatus(response)
	}).then(response => {
		return response.json()
	}).then(jsonData => {
		jsonData.map((factora) => {
			let newRow = dest.insertRow(dest.rows.length)
			const acciones = `
				<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorADetailModal" title='Detalle'>
					<span class="glyphicon glyphicon-list" aria-hidden="true"></span>
				</button>
				<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorAUpdateModal" title='Editar'>
					<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
				</button>
				<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#FactorADeleteModal" title='Eliminar'>
					<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
				</button>`
			newRow.innerHTML = `<td class='font-bold'>${factora.id}</td>
								<td>${factora.descripcion}</td>
								<td>${acciones}</td>`
		})
		if (dest.innerHTML == '') {
			let newRow = dest.insertRow(dest.rows.length)
			newRow.innerHTML = `<td class="text-center" id='blank_row' bgcolor="#FFFFFF" colspan="3">Ningún factor de ajuste creado</td>`
		}
		// setPaginationFactoresAInfo(jsonData.previous, jsonData.next, jsonData.length, jsonData.count)
	}).catch(error => {
		console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
	})
}


/*
 * AddFactorAModal Layout
 */
const divs_create_FactorA = document.getElementById('AddFactorAForm').getElementsByTagName('div')
divs_create_FactorA[0].classList.add('col-md-12')

/*
 * CreateFactorA
 */
document.getElementById('AddFactorAForm').onsubmit = function createFactorA(event) {
	document.querySelector('.messages').innerHTML = ''

	const header_init = {
		'Accept': 'application/json',
		'X-CSRFToken': getCookie("csrftoken")
	}

	const fetchOptions = {
		method: 'POST',
		headers: new Headers(header_init),
		body: new FormData(document.getElementById('AddFactorAForm')),
		credentials: 'same-origin'
	}

	fetch(fda_api_url, fetchOptions).then(response => {
		response.json()
		.then(jsonData => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">El factor de ajuste \"${jsonData.descripcion}\" fue registrado
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`

				// Empty Solicitud form
				document.getElementById('AddFactorAForm').reset()

				$('#AddFactorAModal').modal('hide')
				loadFactoresA(fda_records, fda_api_url)
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
 * UpdateFactorAModal Layout
 */
const divs_update_FactorA = document.getElementById('UpdateFactorAForm').getElementsByTagName('div')
divs_update_FactorA[0].classList.add('col-md-12')


/*
 * UpdateFactorA
 */
 document.getElementById('UpdateFactorAForm').onsubmit = function createFactorA(event) {
	event.preventDefault(); // Evita el auto-envío del botón
	document.querySelector('.messages').innerHTML = ''

	const header_init = {
		'Accept': 'application/json',
		'X-CSRFToken': getCookie("csrftoken")
	}

	const fetchOptions = {
		method: 'PUT',
		headers: new Headers(header_init),
		body: new FormData(document.getElementById('UpdateFactorAForm')),
		credentials: 'same-origin'
	}

	const FactorAId = document.getElementById('FactorAUpdateModalId').innerText;

	fetch(`${fda_api_url}${FactorAId}/`, fetchOptions).then(response => {
		response.json()
		.then(jsonData => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">El factor de ajuste \"${jsonData.descripcion}\" fue actualizado
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`

				// Empty Solicitud form
				document.getElementById('UpdateFactorAForm').reset()

				$('#FactorAUpdateModal').modal('hide')
				loadFactoresA(fda_records, fda_api_url)
				
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
 * FactorAUpdateModal Handler
 */
 $('#FactorAUpdateModal').on('show.bs.modal', (event) => {
	const clickedButton = $(event.relatedTarget);
	const factorAId = clickedButton.closest('tr').find('td:eq(0)').text();

	fetch(`${fda_api_url}${factorAId}`, getAuthorizedFetchOption()).then(response => {
		return checkStatus(response);
	}).then(response => {
		return response.json();
	}).then(jsonData => {
		document.querySelector('#UpdateFactorAForm > div > input[name="descripcion"]').value = jsonData.descripcion;
	}).catch(error => {
		console.log(`Error al realizar fetch de detalle del factor de ajuste Id ${factorAId}: ${error.message}`);
	});
	document.getElementById('FactorAUpdateModalId').innerText = factorAId;
});


document.getElementById('DeleteFactorAForm').onsubmit = function deleteFactorA(event) {
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
	
	const factorAId = document.getElementById('FactorADeleteModalId').innerText;

	fetch(`${fda_api_url}${factorAId}`, fetchOptions).then(response => {
		if(response.ok) {
			// Mostrar mensaje de éxito
			document.querySelector('.messages').innerHTML = `
			<div class="alert alert-dismissable fade in alert-success">El factor de ajuste con Id: ${factorAId} fue eliminado
				<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
			</div>`;
			loadFactoresA(fda_records, fda_api_url);
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
	$('#FactorADeleteModal').modal('hide');
	event.preventDefault(); // Evita el envío POST del botón
	window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
};


/*
 * FactorADeleteModal Handler
 */
 $('#FactorADeleteModal').on('show.bs.modal', (event) => {
	const button = $(event.relatedTarget);
	const FactorAId = button.closest('tr').find('td:eq(0)').text();
	document.getElementById('FactorADeleteModalId').innerText = FactorAId;
});


function loadValoresFactorA() {
	const factora_descr = document.getElementById('ValorFactorAAddModalDesc').innerText;
	const dest = vdfda_records
	// valores_list.innerHTML = ''
	dest.innerHTML = ''
	fetch(`${vdfda_api_url}`, getAuthorizedFetchOption()).then(response => {
		return checkStatus(response)
	}).then(response => {
		return response.json()
	}).then(jsonData => {
		jsonData.map(valor => {
			if(valor.factorDeAjuste_descripcion == factora_descr) {
				let newRow = dest.insertRow(dest.rows.length)
				const acciones = `
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ValorFactorAUpdateModal" title='Editar'>
						<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#ValorFactorADeleteModal" title='Eliminar'>
						<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
					</button>`
					newRow.innerHTML = `<td class='font-bold'>${valor.id}</td>
										<td>${valor.descripcion}</td>
										<td style="display:none;">${valor.factorDeAjuste}</td>
										<td>${acciones}</td>`
			}
		})
		if (dest.innerHTML == '') {
			let newRow = dest.insertRow(dest.rows.length)
			newRow.innerHTML = `<td class="text-center" id='blank_row' bgcolor="#FFFFFF" colspan="3">Ningún valor para el factor de ajuste creado</td>`
		}
	}).catch(error => {
		console.log(`Error al realizar fetch de valores del factor de pc ${factora_descr}: ${error.message}`)
	})
	document.getElementById('FactorADetailModalLabel').innerText = `Detalle del factor de ajuste: \"${factora_descr}\"`
}
/*
 * FactorADetailModalHandler
 */
$('#FactorADetailModal').on('show.bs.modal', (event) => {
	const clickedButton = $(event.relatedTarget)
	document.getElementById('ValorFactorAAddModalId').innerText = clickedButton.closest('tr').find('td:eq(0)').text();
	document.getElementById('ValorFactorAAddModalDesc').innerText = clickedButton.closest('tr').find('td:eq(1)').text();
	loadValoresFactorA();
});
