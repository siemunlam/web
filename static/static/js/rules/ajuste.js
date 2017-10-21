	loadAjustes(ajustes_records, ajuste_api_url)
	$('.nav-tabs a[href="#reglas-ajustes"]').on('show.bs.tab', event => {
		loadAjustes(ajustes_records, ajuste_api_url)
	})

	$('.nav-tabs a[href="#tab-ajustes"]').on('show.bs.tab', event => {
		//TODO: Deberia ser solo cuando esta "active" la tab reglas-ajustes.
		loadAjustes(ajustes_records, ajuste_api_url)
	})

	function loadAjustes(dest, apiURL) {
		dest.innerHTML = ''
		
		fetch(apiURL, getAuthorizedFetchOption()).then(response => {
			return checkStatus(response)
		}).then(response => {
			return response.json()
		}).then(jsonData => {
			jsonData.map((ajuste) => {
				let newRow = dest.insertRow(dest.rows.length)
				newRow.innerHTML = `<td class='font-bold'>${ajuste.id}</td>
									<td>${ajuste.valor}</td>`
			})
			if (dest.innerHTML == '') {
				let newRow = dest.insertRow(dest.rows.length)
				newRow.innerHTML = `<td class="text-center" id='blank_row' bgcolor="#FFFFFF" colspan="3">Ningun ajuste creado</td>`
			}
		}).catch(error => {
			console.log(`Error al realizar fetch a ${apiURL}: ${error.message}`)
		})
    }
