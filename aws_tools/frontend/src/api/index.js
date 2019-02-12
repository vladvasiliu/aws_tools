import axios from 'axios'

const axios_instance = axios.create({
  baseURL: 'http://localhost:8000/api/'
})

export default axios_instance
