<template>
  <div class="login-swiper">
    <!-- <div class="img"> -->
    <form class="form">
     <h2 class="system-title">未来领鲜后台系统</h2>
      <label class="lb" for="name">账号</label>
      <input name="name" id="name" type="text" v-model="userInfo.username" autocomplete="current-password" class="infos"
        @blur="checkRole" autofocus>

      <label for="pwd" class="lb">密码</label>
      <input name="pwd" id="pwd" type="password" v-model="userInfo.password" autocomplete="new-password" class="infos">

      <label for="data" class="lb">身份</label>
      <div class="radio-input">
        <div class="radio-item"><input name="radio" type="radio" class="input" v-model="userInfo.role" :checked="true"
            value="2" />商家</div>
        <div class="radio-item"><input name="radio" type="radio" class="input" v-model="userInfo.role" value="1" />管理员
        </div>
        <div class="radio-item" v-if="isSuper"><input name="radio" type="radio" v-model="userInfo.role" class="input"
            value="0" />
          超管</div>
      </div>
      <!-- <input name="data" id="data" type="date" class="infos"> -->

      <div class="mybtn">
        <div id="send" type="submit" @click="login">登录</div>
        <div id="limpar" type="reset" @click="reset">重置 </div>
      </div>
    </form>

    <!-- </div> -->
    <!-- <div class="login-box">
      <el-form :v-model="userInfo" class="form-box">
        <el-input class="username" v-model="userInfo.username" placeholder="请输入账号" size="large" clearable autofocus
          @blur="checkRole" />
        <el-input class="password" v-model="userInfo.password" type="password" placeholder="请输入密码" size="large"
          show-password />
        <el-radio-group v-model="userInfo.role" class="ml-4">
          <el-radio label="2" size="large">商家</el-radio>
          <el-radio label="1" size="large">管理员</el-radio>
          <el-radio label="0" size="large" v-show="isSuper">超管</el-radio>
        </el-radio-group>
        <div class="login-btn-box">
          <el-button @click="login">登录</el-button>
        </div>
      </el-form>
    </div> -->
  </div>
</template>
<script lang='ts' setup>
import { reactive, ref } from 'vue'
import { ElNotification } from 'element-plus'
import { useRouter } from 'vue-router'
import http from '@/utils/http'
import { useStore } from 'vuex'

const store = useStore()
// 获取router对象
const router = useRouter()
// 用户信息
const userInfo = reactive({
  username: "",
  password: "",
  role: "2"
})
const roleName = ['超级管理员', '管理员', '商家']
// 角色id
// 是否为超管的单选按钮
const isSuper = ref(false)
// 登录按钮对应的函数
const login = () => {
  // const md5: any = new Md5()
  // md5.appendAsciiStr(userInfo.password)
  // userInfo.password = md5.end()
  console.log(userInfo.username, userInfo.password, userInfo.role)


  http.post('/admin/login', {
    username: userInfo.username,
    password: userInfo.password,
    role: userInfo.role
  }
  ).then((res: any) => {
    console.log(res)

    const { sessionid } = res
    // const roleNum = 
    const loginData = {
      username: userInfo.username,
      role: roleName[parseInt(userInfo.role)],
      sessionid
    }
    store.commit('login', loginData)
    ElNotification.success({
      title: '登录成功',
      message: "即将跳转页面",
      duration: 2000,
      position: 'top-right',
    }
    )
    router.push('/home')
  }).catch(() => {
    // router.push('/home')
    userInfo.username = ""
    userInfo.password = ""
    ElNotification.error({
      title: '登录失败',
      message: "请检查用户名和密码",
      position: 'top-right',
    })

  })

}
// 重置
const reset = () => {
  userInfo.username = ''
  userInfo.password = ''
  userInfo.role = "2"
  isSuper.value = false

}
// 检查是否是superAdmin
const checkRole = () => {
  if (userInfo.username === 'superAdmin') {
    isSuper.value = true
  } else {
    isSuper.value = false
  }
}
</script>
<style scoped lang='scss'>
@import url('@/styles/style.scss');

.system-title {
  font-size: 26px;        /* 标题字号 */
  font-weight: bold;      /* 粗体 */
  color: #333;           /* 深灰色文字 */
  text-align: center;     /* 居中对齐 */
  margin: 20px 0 40px;   /* 上下间距控制 */
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1); /* 轻微阴影增加立体感 */
}

.username,
.password {
  height: 50px;
}

.login-swiper {
  width: 100vw;
  height: 100vh;

  background: #bcbdbd;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('@/assets/images/background.png') no-repeat center center fixed;
  background-size: cover;


  .input {
    -webkit-appearance: none;
    /* remove default */
    // display: block;
    margin: 10px;
    width: 24px;
    height: 24px;
    border-radius: 12px;
    cursor: pointer;
    vertical-align: middle;
    box-shadow: hsla(0, 0%, 100%, .15) 0 1px 1px, inset hsla(0, 0%, 0%, .5) 0 0 0 1px;
    background-color: hsla(0, 0%, 0%, .2);
    background-image: -webkit-radial-gradient(hsla(200, 100%, 90%, 1) 0%, hsla(200, 100%, 70%, 1) 15%, hsla(200, 100%, 60%, .3) 28%, hsla(200, 100%, 30%, 0) 70%);
    background-repeat: no-repeat;
    -webkit-transition: background-position .15s cubic-bezier(.8, 0, 1, 1),
      -webkit-transform .25s cubic-bezier(.8, 0, 1, 1);
    outline: none;
  }

  .input:checked {
    -webkit-transition: background-position .2s .15s cubic-bezier(0, 0, .2, 1),
      -webkit-transform .25s cubic-bezier(0, 0, .2, 1);
  }

  .input:active {
    -webkit-transform: scale(1.5);
    -webkit-transition: -webkit-transform .1s cubic-bezier(0, 0, .2, 1);
  }



  /* The up/down direction logic */

  .input,
  .input:active {
    background-position: 0 24px;
  }

  .radio-item {
    font-size: 18px;
    font-weight: bold;
  }

  .input:checked {
    background-position: 0 0;
  }

  .input:checked~.input,
  .input:checked~.input:active {
    background-position: 0 -24px;
  }

  .mybtn {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }

  form {
    // background-color: #444444;
    // border-radius: 10px;
    padding: 60px;
    width: 300px;
    margin: 50px auto;
    border-radius: 50px;
    background: #949896;
    box-shadow: 22px 22px 35px #7a7a7a,
      -22px -22px 35px #bebebe;
  }

  .lb {
    display: block;
    margin-bottom: 10px;
    font-size: 18px;
    font-weight: bold;
  }

  .infos[type="text"],
  input[type="password"],
  input[type="date"] {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: none;
    margin-bottom: 20px;
    background-color: #333333;
    color: white;
  }

  #send {
    --glow-color: rgb(176, 255, 189);
    --glow-spread-color: rgba(123, 255, 160, 0.781);
    --enhanced-glow-color: rgb(182, 175, 71);
    --btn-color: rgba(13, 241, 21, 0.508);
    border: .25em solid var(--glow-color);
    padding: 1em 2em;
    color: var(--glow-color);
    font-size: 16px;
    font-weight: bold;
    background-color: var(--btn-color);
    border-radius: 1em;
    outline: none;
    box-shadow: 0 0 1em .25em var(--glow-color),
      0 0 4em 1em var(--glow-spread-color),
      inset 0 0 .05em .25em var(--glow-color);
    text-shadow: 0 0 .5em var(--glow-color);
    position: relative;
    cursor: pointer;
    transition: all 0.3s;
  }

  #send::after {
    pointer-events: none;
    content: "";
    position: absolute;
    top: 120%;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: var(--glow-spread-color);
    filter: blur(2em);
    opacity: .7;
    transform: perspective(1.5em) rotateX(35deg) scale(1, .6);
  }

  #send:hover {
    color: var(--btn-color);
    background-color: var(--glow-color);
    box-shadow: 0 0 1em .25em var(--glow-color),
      0 0 4em 2em var(--glow-spread-color),
      inset 0 0 .75em .25em var(--glow-color);
  }

  #send:active {
    box-shadow: 0 0 0.6em .25em var(--glow-color),
      0 0 2.5em 2em var(--glow-spread-color),
      inset 0 0 .5em .25em var(--glow-color);
  }

  #limpar {
    --glow-color: rgb(255, 176, 176);
    --glow-spread-color: rgba(255, 123, 123, 0.781);
    --enhanced-glow-color: rgb(182, 175, 71);
    --btn-color: rgba(241, 13, 13, 0.508);
    border: .25em solid var(--glow-color);
    padding: 1em 2em;
    color: var(--glow-color);
    font-size: 16px;
    cursor: pointer;
    font-weight: bold;
    background-color: var(--btn-color);
    border-radius: 1em;
    outline: none;
    box-shadow: 0 0 1em .25em var(--glow-color),
      0 0 4em 1em var(--glow-spread-color),
      inset 0 0 .05em .25em var(--glow-color);
    text-shadow: 0 0 .5em var(--glow-color);
    position: relative;
    transition: all 0.3s;
  }

  #limpar::after {
    pointer-events: none;
    content: "";
    position: absolute;
    top: 120%;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: var(--glow-spread-color);
    filter: blur(2em);
    opacity: .7;
    transform: perspective(1.5em) rotateX(35deg) scale(1, .6);
  }

  #limpar:hover {
    color: var(--btn-color);
    background-color: var(--glow-color);
    box-shadow: 0 0 1em .25em var(--glow-color),
      0 0 4em 2em var(--glow-spread-color),
      inset 0 0 .75em .25em var(--glow-color);
  }

  #limpar:active {
    box-shadow: 0 0 0.6em .25em var(--glow-color),
      0 0 2.5em 2em var(--glow-spread-color),
      inset 0 0 .5em .25em var(--glow-color);
  }


  .login-box {
    width: 50%;
    height: 100vh;
    background: pink;
    display: flex;
    justify-content: center;
    align-items: center;

    .form-box {
      width: 40%;
      // height: 300px;
      background-color: #ccc;

      .login-btn-box {
        text-align: center;
      }
    }
  }
}
</style>