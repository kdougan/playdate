export const jwtLocalStorageKey = 'playDate:jwt';

export function authHeader() {
  // return authorization header with jwt token
  let user = JSON.parse(localStorage.getItem(jwtLocalStorageKey));

  if (user && user.token) {
    return { Authorization: 'Bearer ' + user.token.access_token };
  } else {
    return {};
  }
}
