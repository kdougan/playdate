import axios from 'axios';

export const HTTP = axios.create({
  baseURL: `/api`,
});

export const graphql = (payload, success = null, error = null) => {
  axios({
    method: 'POST',
    url: '/graphql',
    data: payload,
  })
    .then((response) => {
      if (success) success(response.data);
    })
    .error((e) => {
      if (error) error(e);
    });
};
