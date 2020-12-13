import rootState, { RootStateType, HereAddress, PlotDataState } from "./state";

const mutations = {
  updateAddress(state: RootStateType, payload: { address: string }) {
    state.address = payload.address;
  },
  resetAddress(state: RootStateType) {
    state.address = rootState.address;
    state.addressInfo = rootState.addressInfo;
  },
  updateAddressInfo(
    state: RootStateType,
    payload: { addressInfo: HereAddress }
  ) {
    state.addressInfo = payload.addressInfo;
  },
  updatePlotData(state: RootStateType, payload: { plotData: PlotDataState }) {
    state.plotData = payload.plotData;
  },
};

export default mutations;
