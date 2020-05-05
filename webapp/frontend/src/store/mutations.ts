import { RootState } from "./state";

const mutations = {
  updateAddress(state: RootState, payload: { address: string }) {
    state.address = payload.address;
  },
  submitAddress(state: RootState, payload: { addressSubmitted: boolean }) {
    state.addressSubmitted = payload.addressSubmitted;
  }
};

export default mutations;
