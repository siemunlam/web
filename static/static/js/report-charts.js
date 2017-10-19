function saveCategoriaAuxilio(categoria_auxilio, categorias_map) {
  if (categoria_auxilio !== null) {       
      if (categorias_map[categoria_auxilio.descripcion] === undefined) {
          var cat = {
              descripcion: categoria_auxilio.descripcion,
              prioridad: categoria_auxilio.prioridad,
              color: categoria_auxilio.color,
              cantidad: 1
          };
          categorias_map[categoria_auxilio.descripcion] = cat;                   
      } else {
          categorias_map[categoria_auxilio.descripcion].cantidad++;
      }
  }
}

function saveOrigenSolicitud(solicitud, origen_solicitudes_map) {
  if (solicitud !== null) {            
      if (origen_solicitudes_map[solicitud.origen] === undefined) {
          var origen = {
              descripcion: solicitud.origen,
              color: solicitud.origen == 'Web' ? '#ff9f40' : solicitud.origen == 'Agente virtual' ? '#99ff99' : '#9966ff',
              cantidad: 1
          };
          origen_solicitudes_map[solicitud.origen] = origen;                    
      } else {
          origen_solicitudes_map[solicitud.origen].cantidad++;
      }
  }
}

function saveFechaSolicitud(solicitud, fecha_solicitudes_map) {
  if (solicitud !== null) {        
      var fecha_solicitud = moment(solicitud.fecha).format('DD/MM/YY');
      if (fecha_solicitudes_map[fecha_solicitud] === undefined) {
          var fecha = {
              descripcion: fecha_solicitud,
              cantidad: 1
          };
          fecha_solicitudes_map[fecha_solicitud] = fecha;                    
      } else {
          fecha_solicitudes_map[fecha_solicitud].cantidad++;
      }
  }
}

function saveAuxiliosPorEstado(auxilio, categorias_map, estado_auxilio) {
  var estados = auxilio.estados;
  if (!jQuery.isEmptyObject(estados)) {
      var fecha_pendiente = null;
      var fecha_auxilio = null;
      for (var estado in estados) {
          fecha = moment(estados[estado].fecha);
          if (estados[estado].estado === "Pendiente") {
              fecha_pendiente = fecha;
          } else if (estados[estado].estado === estado_auxilio) {
              fecha_auxilio = fecha;
          }
      } 
      if (fecha_pendiente !== null && fecha_auxilio !== null) {
          var dif_minutos = fecha_auxilio.diff(fecha_pendiente, 'minutes');
          // console.log("total de minutos: " + dif_minutos);
          if (categorias_map[auxilio.categoria.descripcion] === undefined) {
              var est = {
                  descripcion: auxilio.categoria.descripcion,
                  color: auxilio.categoria.color,
                  tiempo_total_minutos: dif_minutos,
                  cantidad: 1
              };
              categorias_map[auxilio.categoria.descripcion] = est;     
          } else {
              categorias_map[auxilio.categoria.descripcion].cantidad++;
              categorias_map[auxilio.categoria.descripcion].tiempo_total_minutos += dif_minutos;
          }
      }
  }
}

async function loadAuxilios(api_url) {
  var categorias = {};  
  var origen_solicitudes = {}; 
  var fecha_solicitudes = {}; 
  var auxilios_en_curso = {};
  var auxilios_finalizados = {};
  await fetch(api_url, getAuthorizedFetchOption()).then(response => {
      return checkStatus(response);
  }).then(response => {
      return response.json();
  }).then(jsonData => {
    jsonData.map((auxilio) => { 
      saveCategoriaAuxilio(auxilio.categoria, categorias);
      saveOrigenSolicitud(auxilio.solicitud, origen_solicitudes);
      saveFechaSolicitud(auxilio.solicitud, fecha_solicitudes);
      saveAuxiliosPorEstado(auxilio, auxilios_en_curso, "En curso");
      saveAuxiliosPorEstado(auxilio, auxilios_finalizados, "Finalizado");
    });
  }).catch(error => {
    console.log(`Error al realizar fetch a ${api_url}: ${error.message}`);
  });
  marcarClasificacionAuxiliosGrafico(categorias, "grafico1");
  marcarOrigenSolicitudesGrafico(origen_solicitudes, "grafico2");
  marcarFechaSolicitudesGrafico(fecha_solicitudes, "grafico3");
  marcarTiempoEnColaGrafico(auxilios_en_curso, "grafico4");
  marcarTiempoEnColaGrafico(auxilios_finalizados  , "grafico5");
}

function mostrarMensajeGraficoSinInformacion(elemento) {
    var canvas = document.getElementById(elemento);
    var ctx = canvas.getContext("2d");
    ctx.font = "14px Arial";
    ctx.textAlign = "center";
    ctx.fillText("No hay información para mostrar", canvas.width/2, canvas.height/2); 
}

function setChart(ctx, type, labels, data, color, options, label) {
    var grafico = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color,
                borderColor: color,
                borderWidth: 1
            }]
        },
        options: options
    });
}


function marcarClasificacionAuxiliosGrafico(categorias, elemento) {
    if (!jQuery.isEmptyObject(categorias)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in categorias) {
            label.push(categorias[key].descripcion);
            data.push(categorias[key].cantidad);
            color.push(categorias[key].color);
        }
        setChart(document.getElementById(elemento), 'doughnut', label, data, color, null, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarOrigenSolicitudesGrafico(origen_solicitudes, elemento) {
    if (!jQuery.isEmptyObject(origen_solicitudes)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in origen_solicitudes) {
            label.push(origen_solicitudes[key].descripcion);
            data.push(origen_solicitudes[key].cantidad);
            color.push(origen_solicitudes[key].color);
        }

        var options = {
            legend: {
            "display": false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        };
            
        setChart(document.getElementById(elemento), 'bar', label, data, color, options, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarFechaSolicitudesGrafico(fecha_solicitudes, elemento) {
    if (!jQuery.isEmptyObject(fecha_solicitudes)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in fecha_solicitudes) {
            label.push(fecha_solicitudes[key].descripcion);
            data.push(fecha_solicitudes[key].cantidad);
        }

        var options = {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        };
        setChart(document.getElementById(elemento), 'line', label, data, '#4bc0c0', options, "Total");   
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarTiempoEnColaGrafico(categorias, elemento) {
    if (!jQuery.isEmptyObject(categorias)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in categorias) {
            label.push(categorias[key].descripcion);
            data.push(Math.round(categorias[key].tiempo_total_minutos / categorias[key].cantidad));
            color.push(categorias[key].color);
        }

        var options = {
            legend: {
            "display": false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        };
        setChart(document.getElementById(elemento), 'horizontalBar', label, data, color, options, "Minutos");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}