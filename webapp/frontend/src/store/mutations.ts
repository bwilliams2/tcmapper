import rootState, {
  RootStateType,
  HereAddress,
  PlotDataState,
  MapTypes,
} from "./state";

const mutations = {
  updateAddress(state: RootStateType, payload: { address: string }) {
    state.address = payload.address;
  },
  resetAnalysis(state: RootStateType) {
    state.address = rootState.address;
    state.addressInfo = rootState.addressInfo;
    state.plotControls = rootState.plotControls;
    state.plotData = rootState.plotData;
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
  updateLatLng(state: RootStateType, payload: [number, number]) {
    state.plotControls.latLng = payload;
  },
  updateSelectedUseClasses(state: RootStateType, payload: string[]) {
    state.plotControls.selectedUseClasses = payload;
  },
  updateMapType(state: RootStateType, payload: MapTypes) {
    state.plotControls.mapType = payload;
  },
  updateStartYear(state: RootStateType, payload: number) {
    state.plotControls.startYear = payload;
  },
  updateEndYear(state: RootStateType, payload: number) {
    state.plotControls.endYear = payload;
  },
};

export default mutations;
