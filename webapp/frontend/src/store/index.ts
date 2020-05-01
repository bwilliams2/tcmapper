import Vue from "vue";
import Vuex from "vuex";
import rootState from "./state";
import mutations from "./mutations";
import actions from "./actions";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: rootState,
  mutations: mutations,
  actions: actions,
  modules: {}
});

if (module.hot) {
  // accept actions and mutations as hot modules
  // module.hot.accept(['./mutations', './modules/a'], () => {
  module.hot.accept(["./mutations", "./actions"], () => {
    // require the updated modules
    // have to add .default here due to babel 6 module output
    const newMutations = require("./mutations").default;
    const newActions = require("./actions").default;
    // swap in the new modules and mutations
    store.hotUpdate({
      mutations: newMutations,
      actions: newActions
      // modules: {
      //   a: newModuleA
      // }
    });
  });
}

export default store;
