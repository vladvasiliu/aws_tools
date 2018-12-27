import axios from 'axios'

import auth from '@/auth/'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',
  // Django Rest Framework requires the token format Authorization: Token 1234567890
  // https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
  headers: {'Authorization': 'Token ' + auth.auth.getToken()}
})

export default axiosInstance
