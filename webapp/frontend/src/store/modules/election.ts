import { Commit } from "vuex/types";
import { FeatureItem } from "../state";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface ElectionControlsState {
  properties: string[];
  selectedPatternProperty: string | null;
  selectedColorProperty: string | null;
}

export interface ElectionDataState {
  features: FeatureItem[];
}

interface State {
  controls: ElectionControlsState;
  data: ElectionDataState;
}

const state: State = {
  controls: {
    properties: [],
    selectedPatternProperty: null,
    selectedColorProperty: null,
  },
  data: {
    features: [],
  },
};

const actions = {
  async updateParcels({ commit, state }: { commit: Commit; state: State }) {
    commit("updateShowLoadingOverlay", true, { root: true });
    return axios
      .get(`${API_URL}/api/election/metroprecincts`, {
        timeout: 50000,
      })
      .then((res) => {
        commit("updateShowLoadingOverlay", false, { root: true });
        commit("updateFullParcels", JSON.parse(res.data));
      });
  },
};

const mutations = {
  updateFullParcels(state: State, payload: FeatureItem[]) {
    state.data.features = payload;
    if (payload.length > 0) {
      state.controls.properties = Object.keys(payload[0].properties);
      state.controls.selectedColorProperty = "2016-2020";
    }
  },
  updateParcelProperty(state: State, payload: string) {
    state.controls.selectedColorProperty = payload;
  },
};

const getters = {
  features: (state: State) => {
    return state.data.features;
  },
  properties: (state: State) => {
    return state.controls.properties;
  },
  selectedColorProperty: (state: State) => {
    return state.controls.selectedColorProperty;
  },
  selectedPatternProperty: (state: State) => {
    return state.controls.selectedPatternProperty;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
