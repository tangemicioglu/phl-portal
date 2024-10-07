import axios from 'axios';

const ROOT_API = process.env.VUE_APP_ROOT_API;

async function login(username: string, password: string) {
  const path = `${ROOT_API}/tokens`;
  const auth = { auth: { username, password } };
  const response = await axios.post(path, {}, auth);
  return response.data;
}

async function register(email: string, username: string, password: string) {
  const path = `${ROOT_API}/users`;
  const payload = { email, username, password };
  const response = await axios.post(path, payload);
  return response.data;
}

export default { login, register };
