import axios from 'axios';
export const HTTP = axios.create({
  baseURL: `http://0.0.0.0:5000/api`,
});
