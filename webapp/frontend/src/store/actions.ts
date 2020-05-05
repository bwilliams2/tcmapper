import { Commit } from "vuex/types";

const rootActions = {
  updateAddress({ commit }: { commit: Commit }, address: string) {
    commit("updateAddress", { address: address });
  },
  submitAddress({ commit }: { commit: Commit }, newState: boolean) {
    commit("submitAddress", { addressSubmitted: newState });
  }
};

export default rootActions;
