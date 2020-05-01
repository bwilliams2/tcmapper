import { RootState } from "./state";

const mutations = {
  updateAddress(state: RootState, payload: { address: string }) {
    state.address = payload.address;
  }
};

export default mutations;
