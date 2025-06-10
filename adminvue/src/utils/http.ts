import axios, { AxiosInstance, AxiosResponse } from 'axios'
const http: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000,
})
// 添加请求拦截器
http.interceptors.request.use(
  (config: any) => {
    // 在发送请求之前做些什么
    if (config.url !== '/admin/login') {
      config.headers['Authorization'] =
        'Beaner ' + localStorage.getItem('sessionid')
    }
    if (!config.headers['Content-Type']) {
      // 如果没有设置请求头
      if (config.method === 'post') {
        config.headers['content-type'] = 'application/json' // post 请求
      } else {
        config.headers['content-type'] = 'application/x-www-from-urlencoded' // 默认类型
      }
    }
    // console.log(config.url)
    // console.log('请求发送了', config)
    return config
  },
  (error: any) => {
    // 处理请求错误
    return Promise.reject(error)
  }
)
// 添加响应拦截器
http.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    if (response.status === 200) {
      return response.data
    }
  },
  (error: any) => {
    // 处理响应错误
    console.log('请求失败了', error)
    return Promise.reject(error)
  }
)
export default http
