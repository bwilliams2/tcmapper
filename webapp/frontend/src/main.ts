import App from "./components/App.vue";
import router from "./router";
import store from "./store";
import vuetify from "@/plugins/vuetify";
import Vue from "vue";
import "leaflet/dist/leaflet.css";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
