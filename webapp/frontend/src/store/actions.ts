import { Commit } from "vuex/types";
import { HereAddress } from "./state";

const rootActions = {
  updateAddress({ commit }: { commit: Commit }, address: string) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commit("updateAddress", { address: address });
        resolve();
      }, 1000);
    });
  },
  updateAddressInfo({ commit }: { commit: Commit }, addressInfo: HereAddress) {
    commit("updateAddressInfo", { addressInfo: addressInfo });
  },
};

export default rootActions;
