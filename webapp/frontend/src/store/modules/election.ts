import { Commit } from "vuex/types";
import { FeatureItem } from "../state";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface ElectionControlsState {
  properties: string[];
  selectedProperty: string | null;
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
    selectedProperty: null,
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
    }
  },
  updateParcelProperty(state: State, payload: string) {
    state.controls.selectedProperty = payload;
  },
};

const getters = {
  features: (state: State) => {
    return state.data.features;
  },
  properties: (state: State) => {
    return state.controls.properties;
  },
  selectedProperty: (state: State) => {
    return state.controls.selectedProperty;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
