import { createStore } from 'vuex'

export default createStore({
  state: {
    addModelFlag: false,
    userInfo: {
      username: '',
      role: '',
      sessionid: '',
    },
  },
  getters: {},
  mutations: {
    // 更改增加口味和类别的显示框状态
    ShowModel(state) {
      state.addModelFlag = !state.addModelFlag
    },
    login({ userInfo }, data) {
      console.log('当前store更新了', data)
      localStorage.setItem('sessionid', data.sessionid)
      userInfo.sessionid = data.sessionid
      userInfo.username = data.username
      userInfo.role = data.role
      localStorage.setItem('loginUser', JSON.stringify(data))
    },
    logout({ userInfo }) {
      userInfo.sessionid = ''
      userInfo.role = ''
      userInfo.username = ''
      localStorage.removeItem('sessionid')
      localStorage.removeItem('loginUser')
      console.log('vuex清空了数据')
    },
  },
  actions: {},
  modules: {},
})
