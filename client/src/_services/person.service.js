import { config, jwtLocalStorageKey } from '../_helpers';

export const personService = {
  login,
  logout,
  handleResponse,
};

function handleResponse(response) {
  return response.text().then((text) => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      if (response.status === 401) {
        logout();
        location.reload(true);
      }
      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }
    return data;
  });
}

function login(email, password) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  };
  return fetch(`${config.apiUrl}/v1/auth`, requestOptions)
    .then(handleResponse)
    .then((person) => {
      if (person.token) {
        localStorage.setItem(jwtLocalStorageKey, JSON.stringify(person));
      }
      return person;
    });
}

function logout() {
  localStorage.removeItem(jwtLocalStorageKey);
}
