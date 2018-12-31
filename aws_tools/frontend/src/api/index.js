import axios from 'axios'
import auth from '@/auth/'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/'
})

if (auth.state.isAuthenticated) {
  axiosInstance.defaults.headers.common['Authorization'] = 'Token ' + auth.state.token
}

export default axiosInstance
