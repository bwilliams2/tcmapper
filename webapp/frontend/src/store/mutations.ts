import { RootState, HereAddress } from "./state";

const mutations = {
  updateAddress(state: RootState, payload: { address: string }) {
    state.address = payload.address;
  },
  updateAddressInfo(state: RootState, payload: { addressInfo: HereAddress }) {
    state.addressInfo = payload.addressInfo;
  }
};

export default mutations;
