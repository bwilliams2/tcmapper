import App from "./components/App.vue";
import router from "./router";
import store from "./store";
import vuetify from "@/plugins/vuetify";
import Vue from "vue";
import VueScrollactive from "vue-scrollactive";
import "leaflet/dist/leaflet.css";

Vue.config.productionTip = false;
Vue.use(VueScrollactive);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
