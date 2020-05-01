import { Commit } from "vuex/types";

const rootActions = {
  updateAddress({ commit }: { commit: Commit }, address: string) {
    commit("updateAddress", { address: address });
  }
};

export default rootActions;
