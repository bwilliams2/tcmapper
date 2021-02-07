import { Commit } from "vuex/types";
import { FeatureItem } from "../state";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface ParcelControlsState {
  properties: string[];
  selectedProperty: string | null;
}

export interface ParcelDataState {
  features: FeatureItem[];
}

export interface State {
  controls: ParcelControlsState;
  data: ParcelDataState;
}

const state = {
  features: {
    properties: [],
    selectedProperty: null,
  },
  data: {
    features: [],
  },
};

const actions = {
  updateParcels({ commit, state }: { commit: Commit; state: State }) {
    return axios
      .get(`${API_URL}/api/fullparcels`, {
        timeout: 50000,
      })
      .then((res: { data: FeatureItem[] }) => {
        commit("updateFullParcels", res.data);
      });
  },
};

const mutations = {
  updateFullParcels(state: State, payload: FeatureItem[]) {
    state.data.features = payload;
    if (payload.length > 0) {
      state.controls.properties = Object.keys(state.data.features);
    }
  },
  updateParcelProperty(state: State, payload: string) {
    state.controls.selectedProperty = payload;
  },
};

export default {
  namespaced: true,
  state,
  // getters,
  actions,
  mutations,
};
