import axios from "axios";
import { API_URL } from "@/utils/misc";
import { Commit } from "vuex/types";
import { RootStateType } from "../state";

export interface State {
  controls: {
    meanAge: number | null;
    meanEMV: number | null;
    cityDis: number | null;
  };
  limits: {
    meanAge: [number, number];
    meanEMV: [number, number];
    cityDis: [number, number];
  };
  data: {
    closestIDs: number[];
    predictedMargin: number;
    closestData: Record<string, string | number>[];
  };
}

const state: State = {
  controls: {
    meanAge: null,
    meanEMV: null,
    cityDis: null,
  },
  limits: {
    meanAge: [1974, 2003],
    meanEMV: [150000, 300000],
    cityDis: [0.5, 30],
  },
  data: {
    closestIDs: [],
    predictedMargin: 0,
    closestData: [],
  },
};

interface ActionArgument {
  commit: Commit;
  state: State;
}

const actions = {
  async makePrediction({ commit, state }: ActionArgument) {
    return axios
      .get(`${API_URL}/api/election/model`, {
        params: { ...state.controls },
        timeout: 50000,
      })
      .then((res) => {
        const data: State["data"] = JSON.parse(res.data);
        commit("updateModelData", data);
      });
  },
  async updateControlLimits({ commit, state }: ActionArgument) {
    return axios
      .get(`${API_URL}/api/election/modelLimits`, {
        timeout: 5000,
      })
      .then((res) => {
        commit("updateModelControlLimits", JSON.parse(res.data));
      });
  },
  updateMeanAge({ commit, state }: ActionArgument, newAge: number) {
    commit("updateMeanAge", newAge);
  },
  updateMeanEMV({ commit, state }: ActionArgument, newEMV: number) {
    commit("updateMeanEMV", newEMV);
  },
  updateCityDis({ commit, state }: ActionArgument, cityDis: number) {
    commit("updateCityDis", cityDis);
  },
};

const mutations = {
  updateModelData(state: State, payload: State["data"]) {
    state.data = { ...payload };
  },
  updateModelControlLimits(state: State, payload: State["limits"]) {
    state.limits = { ...payload };
  },
  updateMeanAge(state: State, payload: number) {
    state.controls.meanAge = payload;
  },
  updateMeanEMV(state: State, payload: number) {
    state.controls.meanEMV = payload;
  },
  updateCityDis(state: State, payload: number) {
    state.controls.cityDis = payload;
  },
};

const getters = {
  metroFeatures: (state: State, rootState: RootStateType) => {
    const counties = [
      "Anoka",
      "Dakota",
      "Hennepin",
      "Scott",
      "Ramsey",
      "Washington",
      "Carver",
    ];
    return rootState.election?.data.features.filter(
      (el) =>
        counties.includes(el?.properties.countyname) &&
        el.properties.year === 2020
    );
  },
  meanAge: (state: State) => {
    return state.controls.meanAge;
  },
  meanEMV: (state: State) => {
    return state.controls.meanEMV;
  },
  cityDis: (state: State) => {
    return state.controls.cityDis;
  },
  meanAgeLimits: (state: State) => {
    return state.limits.meanAge;
  },
  meanEMVLimits: (state: State) => {
    return state.limits.meanEMV;
  },
  cityDisLimits: (state: State) => {
    return state.limits.cityDis;
  },
  closetIDs: (state: State) => {
    return state.data.closestIDs;
  },
  closetData: (state: State) => {
    return state.data.closestData;
  },
  predictedMargin: (state: State) => {
    return state.data.predictedMargin;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
