import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000/api'  // Alterado para a porta 3000
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  console.log('Token being sent:', token); // Log do token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('Full Authorization header:', config.headers.Authorization); 
  } else {
    console.warn('No token found in localStorage');
  }
  return config;
});

// Função para buscar notícias de um ativo
const buscarNoticias = async (ticker) => {
  try {
    const response = await axios.post('http://localhost:5000/noticias', { ticker });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar notícias:', error);
    throw error;
  }
};

export { api, buscarNoticias };