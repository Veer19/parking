import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'

Vue.config.productionTip = false
import VueGeolocation from 'vue-browser-geolocation';
import * as VueGoogleMaps from "vue2-google-maps";
Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyDqj1Z5-UAGiKxYHdK8XXosU2RS9Pey3Rw",
    libraries: "places" // necessary for places input
  }
});
Vue.use(VueGeolocation);
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
