import axios, { AxiosError } from 'axios';
import { authHeader, formDataHeader } from '../helpers/headers';

const ROOT_API = process.env.VUE_APP_ROOT_API;

async function uploadScore(title, composer, file, token) {
  const path = `${ROOT_API}/score`;
  const payload = new FormData();
  payload.append('title', title);
  payload.append('composer', composer);
  payload.append('file', file);
  try {
    const response = await axios.post(path, payload, { headers: formDataHeader(token) });
    return response.data;
  } catch (error) {
    throw error as AxiosError;
  }
}

async function getScores(token) {
  const path = `${ROOT_API}/scores`;
  const response = await axios.get(path, { headers: authHeader(token) });
  return response.data;
}

async function getXML(score, token) {
  const path = `${ROOT_API}/score/${score}`;
  const response = await axios.get(path, { headers: authHeader(token) });
  return response.data;
}

async function uploadRecording(midi, score, token) {
  const path = `${ROOT_API}/score/${score}/midi`;
  const payload = new FormData();
  payload.append('file', midi);
  try {
    const response = await axios.post(path, payload, { headers: formDataHeader(token) });
    return response.data;
  } catch (error) {
    throw error as AxiosError;
  }
}

async function getRecording(midi, token) {
  const path = `${ROOT_API}/midi/${midi}`;
  const response = await axios.get(path, { headers: authHeader(token) });
  return response.data;
}

export default {
  uploadScore, getScores, getXML, uploadRecording, getRecording,
};
