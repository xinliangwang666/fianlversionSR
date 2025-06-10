import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-plus/dist/index.css'

window.ResizeObserver = class _NewResizeObserver extends ResizeObserver {
  constructor(callback: any) {
    super((...rest) =>
      window.requestAnimationFrame(() => callback.apply(this, rest))
    )
  }
}

createApp(App).use(store).use(router).mount('#app')
