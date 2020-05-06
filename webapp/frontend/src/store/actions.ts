import { Commit } from "vuex/types";
import { HereAddress } from "./state";

const rootActions = {
  updateAddress({ commit }: { commit: Commit }, address: string) {
    commit("updateAddress", { address: address });
  },
  updateAddressInfo({ commit }: { commit: Commit }, addressInfo: HereAddress) {
    commit("updateAddressInfo", { addressInfo: addressInfo });
  }
};

export default rootActions;
