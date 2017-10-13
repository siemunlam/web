	loadCategorias(categorias_records, categoria_api_url)
	$('.nav-tabs a[href="#reglas-categorias"]').on('show.bs.tab', event => {
		loadCategorias(categorias_records, categoria_api_url)
	})

	function loadCategorias(dest, apiURL) {
		dest.innerHTML = ''
		
		fetch(apiURL, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response)
		}).then(response => {
			return response.json()
		}).then(jsonData => {
			jsonData.results.map((categoria) => {
				let newRow = dest.insertRow(dest.rows.length)
				const acciones = `
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#CategoryUpdateModal" title='Editar'>
						<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-transparent btn-xs" data-toggle="modal" data-target="#CategoryDeleteModal" title='Eliminar'>
						<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
					</button>`
				newRow.innerHTML = `<td class='font-bold' bgcolor='${categoria.color}'>${categoria.id}</td>
									<td>${categoria.descripcion}</td>
									<td>${categoria.prioridad}</td>
									<td>${acciones}</td>`
			})
			setPaginationCategoriasInfo(jsonData.previous, jsonData.next, jsonData.results.length, jsonData.count)
		}).catch(error => {
			console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
		})
    }
    

    function setPaginationCategoriasInfo(previous, next, currentAmount, totalAmount) {
		document.getElementById('CategoriaCurrentPageAmount').innerText = currentAmount
		document.getElementById('CategoriaTotalAmount').innerText = totalAmount

		if(previous === null)
			document.querySelector('#categoriasPager > .previous').classList.add('disabled')
		else {
			document.querySelector('#categoriasPager > .previous').classList.remove('disabled')
			document.querySelector('#categoriasPager > .previous > a').link = previous
		}
		if(next === null)
			document.querySelector('#categoriasPager > .next').classList.add('disabled')
		else {
			document.querySelector('#categoriasPager > .next').classList.remove('disabled')
			document.querySelector('#categoriasPager > .next > a').link = next
		}
    }
    

	/*
	 * AddCategoryModal Layout
	 */
	const divs_create_category = document.getElementById('AddCategoryForm').getElementsByTagName('div')
	divs_create_category[0].classList.add('col-md-12')
	divs_create_category[1].classList.add('col-md-6')
	divs_create_category[1].getElementsByTagName('input')[0].classList.add('text-center', 'font-bold')
	divs_create_category[2].classList.add('col-md-6')

	/*
	 * CreateCategory
	 */
	document.getElementById('AddCategoryForm').onsubmit = function createCategory(event) {
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'POST',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('AddCategoryForm')),
			credentials: 'same-origin'
		}

		fetch(categoria_api_url, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La categoría \"${jsonData.descripcion}\" fue registrada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('AddCategoryForm').reset()

					$('#AddCategoryModal').modal('hide')
					loadCategorias(categorias_records, categoria_api_url)
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
	 * UpdateCategoryModal Layout
	 */
	const divs_update_category = document.getElementById('UpdateCategoryForm').getElementsByTagName('div')
	divs_update_category[0].classList.add('col-md-12')
	divs_update_category[1].classList.add('col-md-6')
	divs_update_category[1].getElementsByTagName('input')[0].classList.add('text-center', 'font-bold')
	divs_update_category[2].classList.add('col-md-6')


	/*
	 * UpdateCategory
	 */
	 document.getElementById('UpdateCategoryForm').onsubmit = function createCategory(event) {
		event.preventDefault(); // Evita el auto-envío del botón
		document.querySelector('.messages').innerHTML = ''

		const header_init = {
			'Accept': 'application/json',
			'X-CSRFToken': getCookie("csrftoken")
		}

		const fetchOptions = {
			method: 'PUT',
			headers: new Headers(header_init),
			body: new FormData(document.getElementById('UpdateCategoryForm')),
			credentials: 'same-origin'
		}

		const categoryId = document.getElementById('CategoryUpdateModalId').innerText;

		fetch(`${categoria_api_url}${categoryId}/`, fetchOptions).then(response => {
			response.json()
			.then(jsonData => {
				if(response.ok) {
					// Mostrar mensaje de éxito
					document.querySelector('.messages').innerHTML = `
					<div class="alert alert-dismissable fade in alert-success">La categoría \"${jsonData.descripcion}\" fue actualizada
						<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					</div>`

					// Empty Solicitud form
					document.getElementById('UpdateCategoryForm').reset()

					$('#CategoryUpdateModal').modal('hide')
					loadCategorias(categorias_records, categoria_api_url)
					
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
	 * CategoryUpdateModal Handler
	 */
	 $('#CategoryUpdateModal').on('show.bs.modal', (event) => {
		const clickedButton = $(event.relatedTarget);
		const categoriaId = clickedButton.closest('tr').find('td:eq(0)').text();

		fetch(`${categoria_api_url}${categoriaId}`, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response);
		}).then(response => {
			return response.json();
		}).then(jsonData => {
			document.querySelector('#UpdateCategoryForm > div > input[name="descripcion"]').value = jsonData.descripcion;
			document.querySelector('#UpdateCategoryForm > div > input[name="prioridad"').value = jsonData.prioridad;
			document.querySelector('#UpdateCategoryForm > div > input[name="color"').value = jsonData.color;
		}).catch(error => {
			console.log(`Error al realizar fetch de detalle de la categoría Id ${categoriaId}: ${error.message}`);
		});
		document.getElementById('CategoryUpdateModalId').innerText = categoriaId;
	});
	

	document.getElementById('DeleteCategoryForm').onsubmit = function deleteCategory(event) {
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
		
		const categoriaId = document.getElementById('CategoryDeleteModalId').innerText;

		fetch(`${categoria_api_url}${categoriaId}`, fetchOptions).then(response => {
			if(response.ok) {
				// Mostrar mensaje de éxito
				document.querySelector('.messages').innerHTML = `
				<div class="alert alert-dismissable fade in alert-success">Categoría con Id: ${categoriaId} fue eliminada
					<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
				</div>`;
				loadCategorias(categorias_records, categoria_api_url);
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
		$('#CategoryDeleteModal').modal('hide');
		event.preventDefault(); // Evita el envío POST del botón
		window.scrollTo(0,0); // Scroll a la parte superior de la pantalla
	};


	/*
	 * CategoryDeleteModal Handler
	 */
	 $('#CategoryDeleteModal').on('show.bs.modal', (event) => {
		const button = $(event.relatedTarget);
		const categoryId = button.closest('tr').find('td:eq(0)').text();
		document.getElementById('CategoryDeleteModalId').innerText = categoryId;
	});
