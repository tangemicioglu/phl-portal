function authHeader(token) {
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
}

function formDataHeader(token) {
  if (token) {
    return {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    };
  }
  return { 'Content-Type': 'multipart/form-data' };
}

export { authHeader, formDataHeader };
