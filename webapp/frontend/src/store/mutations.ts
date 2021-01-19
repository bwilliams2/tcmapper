import rootState, {
  RootStateType,
  HereAddress,
  PlotDataState,
  MapTypes,
  genRootState,
} from "./state";

const mutations = {
  updateAddress(state: RootStateType, payload: { address: string }) {
    state.address = payload.address;
  },
  resetAnalysis(state: RootStateType) {
    // state.address = rootState.address;
    // state.addressInfo = rootState.addressInfo;
    // state.plotControls = rootState.plotControls;
    // state.plotData = rootState.plotData;
    state.plotControls.latLng = [null, null];
    state.plotControls.endYear = rootState.plotControls.endYear;
    state.plotControls.startYear = rootState.plotControls.startYear;
    state.plotControls.analysisRange = rootState.plotControls.analysisRange;
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
    const { plotData } = payload;
    plotData.useClasses = plotData.useClasses.sort();
    state.plotData = { ...state.plotData, ...payload.plotData };
  },
  updateMetroCounties(
    state: RootStateType,
    payload: PlotDataState["counties"]
  ) {
    state.plotData.counties = payload;
  },
  updateAnalysisRange(state: RootStateType, payload: number) {
    state.plotControls.analysisRange = payload;
  },
  updateLatLng(state: RootStateType, payload: [number, number]) {
    state.plotControls.latLng = payload;
  },
  updateSelectedUseClasses(state: RootStateType, payload: string[]) {
    state.plotControls.selectedUseClasses = payload.sort();
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
