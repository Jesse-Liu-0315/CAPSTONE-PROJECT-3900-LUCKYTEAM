import config from '../config.json';

// Make request to server
const makeRequest = (route, method, body, token) => {
  // Request options
  const requestOptions = {
    method: method,
    headers: {  'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
  }
  // Request body
  if (body !== undefined) {
    requestOptions.body = JSON.stringify(body);
  }
  // Request token
  if (token !== undefined) {
    requestOptions.headers.Authorization = token;
  }

  return new Promise((resolve, reject) => {
    fetch(`http://localhost:${config.BACKEND_PORT}` + route, requestOptions)
      .then(rawresponse => rawresponse.json())
      .then(response => {
        if (response.error) {
          reject(response.error);
        } else {
          resolve(response);
        }
      })
      .catch(error => {
        alert(error);
      });
  });
}

export default makeRequest;
