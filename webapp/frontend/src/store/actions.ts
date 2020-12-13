import { Commit } from "vuex/types";
import axios from "axios";
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
  updateAddressInfo(
    { commit, state }: { commit: Commit; state: RootStateType },
    addressInfo: HereAddress
  ) {
    commit("updateAddressInfo", { addressInfo: addressInfo });
    return axios
      .get("api/weight", {
        params: {
          longitude: addressInfo.position.lng,
          latitude: addressInfo.position.lat,
          radius: state.analysisDistance,
        },
      })
      .then((res) => {
        const locationData = JSON.parse(res.data.locationData);
        const histData = JSON.parse(res.data.histData);
        const yearData = JSON.parse(res.data.yearData);
        const weightData = JSON.parse(res.data.weightData);
        commit("updatePlotData", {
          plotData: { locationData, histData, yearData, weightData },
        });
      });
  },
};

export default rootActions;
