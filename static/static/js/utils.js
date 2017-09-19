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