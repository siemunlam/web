/*
 *    Django Documentation 1.11 cookie handler
 *	  from: https://docs.djangoproject.com/en/1.11/ref/csrf/
 */
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie != '') {
      const cookies = document.cookie.split(';')
      for (var i = 0; i < cookies.length; i++) {
          let cookie = jQuery.trim(cookies[i])
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
              break
          }
      }
  }
  return cookieValue
};

function checkStatus(response) {
  if(response.ok)
    return Promise.resolve(response);
  else
    return Promise.reject(new Error(response.statusText));
};

function getAuthorizedFetchOption() {
  const header_init = {
    'Accept': 'application/json',
    'X-CSRFToken': getCookie("csrftoken")
  }
  fetchOptions = {
    method: 'GET',
    headers: new Headers(header_init),
    credentials: 'same-origin'
  };
  return fetchOptions
};