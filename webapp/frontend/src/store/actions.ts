import { Commit } from "vuex/types";
import axios from "axios";
import { API_URL } from "../utils/misc";
import rootState, { HereAddress, PlotDataState, RootStateType } from "./state";

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
  updateAddressInfo(
    { commit, state }: { commit: Commit; state: RootStateType },
    addressInfo: HereAddress
  ) {
    commit("updateAddressInfo", { addressInfo: addressInfo });
    commit("updateShowLoadingOverlay", true);
    return axios
      .get(`${API_URL}/api/weight`, {
        params: {
          longitude: addressInfo.position.lng,
          latitude: addressInfo.position.lat,
          radius: state.plotControls.analysisRange,
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
  },
  updatePlotData({ commit, state }: { commit: Commit; state: RootStateType }) {
    commit("updateShowLoadingOverlay", true);
    const lat = state.plotControls.latLng[0];
    const lng = state.plotControls.latLng[1];
    if (lat && lng) {
      return axios
        .get(`${API_URL}/api/weight`, {
          params: {
            longitude: lng,
            latitude: lat,
            radius: state.plotControls.analysisRange,
          },
          timeout: 50000,
        })
        .then((res) => {
          const locationData = JSON.parse(res.data.locationData);
          const histData = JSON.parse(res.data.histData);
          const yearData = JSON.parse(res.data.yearData);
          const weightData = JSON.parse(res.data.weightData);
          const features = JSON.parse(res.data.features);
          const useClasses = JSON.parse(res.data.useClasses);
          commit("updatePlotData", {
            plotData: {
              locationData,
              histData,
              yearData,
              weightData,
              features,
              useClasses,
            },
          });
          commit("updateSelectedUseClasses", useClasses);
          commit("updateShowLoadingOverlay", false);
        });
    } else {
      commit("updateShowLoadingOverlay", false);
    }
  },
  updateAnalysisRange(
    { commit, state }: { commit: Commit; state: RootStateType },
    newValue: number
  ) {
    commit("updateShowLoadingOverlay", true);
    commit("updateAnalysisRange", newValue);
    return axios
      .get(`${API_URL}/api/weight`, {
        params: {
          longitude: state.addressInfo.position.lng,
          latitude: state.addressInfo.position.lat,
          radius: newValue,
        },
        timeout: 50000,
      })
      .then((res) => {
        const locationData = JSON.parse(res.data.locationData);
        const histData = JSON.parse(res.data.histData);
        const yearData = JSON.parse(res.data.yearData);
        const weightData = JSON.parse(res.data.weightData);
        const features = JSON.parse(res.data.features);
        const useClasses = JSON.parse(res.data.useClasses);
        commit("updatePlotData", {
          plotData: {
            locationData,
            histData,
            yearData,
            weightData,
            features,
            useClasses,
          },
        });
        commit("updateSelectedUseClasses", useClasses);
        commit("updateShowLoadingOverlay", false);
      });
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
