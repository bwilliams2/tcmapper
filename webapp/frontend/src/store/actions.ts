import { Commit } from "vuex/types";
import axios from "axios";
import { API_URL } from "../utils/misc";
import rootState, { HereAddress, PlotDataState, RootStateType } from "./state";
import { json } from "d3";

const updatePlotData = async (
  commit: Commit,
  lng: number,
  lat: number,
  radius: number
) => {
  return axios
    .get(`${API_URL}/api/weight`, {
      params: {
        longitude: lng,
        latitude: lat,
        radius,
      },
      timeout: 50000,
    })
    .then((res) => {
      const locationData = JSON.parse(res.data.locationData);
      const histData = JSON.parse(res.data.histData);
      const yearData = JSON.parse(res.data.yearData);
      const weightData = JSON.parse(res.data.weightData);
      const features = JSON.parse(res.data.features);
      const growthData = JSON.parse(res.data.growthData);
      const useClasses = JSON.parse(res.data.useClasses);
      commit("updatePlotData", {
        plotData: {
          locationData,
          histData,
          growthData,
          yearData,
          weightData,
          features,
          useClasses,
        },
      });
      commit("updateSelectedUseClasses", useClasses);
      commit("updateShowLoadingOverlay", false);
    });
};

const getMetroCounties = async (commit: Commit) => {
  return axios
    .get(`${API_URL}/api/counties`, {
      timeout: 50000,
    })
    .then((res) => {
      const counties = JSON.parse(res.data.counties);
      commit("updateMetroCounties", counties);
      // commit("updateShowLoadingOverlay", false);
    });
};

const rootActions = {
  updateAddress({ commit }: { commit: Commit }, address: string) {
    return new Promise<void>((resolve) => {
      setTimeout(() => {
        commit("updateAddress", { address: address });
        resolve();
      }, 5000);
    });
  },
  resetAddress({ commit }: { commit: Commit }) {
    commit("resetAddress");
  },
  updateShowLoadingOverlay({ commit }: { commit: Commit }, newState: boolean) {
    commit("updateShowLoadingOverlay", newState);
  },
  async updateAddressInfo(
    { commit, state }: { commit: Commit; state: RootStateType },
    addressInfo: HereAddress
  ) {
    commit("updateAddressInfo", { addressInfo: addressInfo });
    commit("updateShowLoadingOverlay", true);
    const lat = state.plotControls.latLng[0];
    const lng = state.plotControls.latLng[1];
    const radius = state.plotControls.analysisRange;
    return updatePlotData(commit, lng as number, lat as number, radius);
  },
  async updateMetroCounties({ commit }: { commit: Commit }) {
    // commit("updateShowLoadingOverlay", true);
    return getMetroCounties(commit);
  },
  async updatePlotData({
    commit,
    state,
  }: {
    commit: Commit;
    state: RootStateType;
  }) {
    commit("updateShowLoadingOverlay", true);
    const lat = state.plotControls.latLng[0];
    const lng = state.plotControls.latLng[1];
    if (lat && lng) {
      return updatePlotData(commit, lng, lat, state.plotControls.analysisRange);
    } else {
      commit("updateShowLoadingOverlay", false);
    }
  },
  async updateAnalysisRange(
    { commit, state }: { commit: Commit; state: RootStateType },
    newValue: number
  ) {
    commit("updateShowLoadingOverlay", true);
    commit("updateAnalysisRange", newValue);
    const lat = state.plotControls.latLng[0];
    const lng = state.plotControls.latLng[1];
    if (lat && lng) {
      return updatePlotData(commit, lng, lat, state.plotControls.analysisRange);
    } else {
      commit("updateShowLoadingOverlay", false);
    }
  },
  updateLatLng({ commit }: { commit: Commit }, newLatLng: [number, number]) {
    commit("updateLatLng", newLatLng);
  },
  updateSelectedUseClasses({ commit }: { commit: Commit }, newValue: string[]) {
    commit("updateSelectedUseClasses", newValue);
  },
  updateStartYear({ commit }: { commit: Commit }, newValue: number) {
    commit("updateStartYear", newValue);
  },
  updateEndYear({ commit }: { commit: Commit }, newValue: number) {
    commit("updateEndYear", newValue);
  },
  updateMapType({ commit }: { commit: Commit }, newValue: number) {
    commit("updateMapType", newValue);
  },
  resetAnalysis({ commit }: { commit: Commit }) {
    commit("resetAnalysis");
  },
};

export default rootActions;
