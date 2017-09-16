function checkStatus(response) {
    if(response.ok)
      return Promise.resolve(response);
    else
      return Promise.reject(new Error(response.statusText));
  };