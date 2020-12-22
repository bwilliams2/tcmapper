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
  updateShowLoadingOverlay(state: RootStateType, payload: boolean) {
    state.ui.showLoadingOverlay = payload;
  },
  updatePlotData(state: RootStateType, payload: { plotData: PlotDataState }) {
    state.plotData = payload.plotData;
  },
  updateAnalysisRange(state: RootStateType, payload: number) {
    state.plotControls.analysisRange = payload;
  },
  updateStartYear(state: RootStateType, payload: number) {
    state.plotControls.startYear = payload;
  },
  updateEndYear(state: RootStateType, payload: number) {
    state.plotControls.endYear = payload;
  },
};

export default mutations;
