import { Commit } from "vuex/types";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface PrecinctProperties extends Record<string, unknown> {
  year: number;
}

export type PrecinctItem = GeoJSON.Feature<GeoJSON.Polygon, PrecinctProperties>;
export interface ElectionControlsState {
  properties: string[];
  selectedYear: number | null;
  selectedPatternProperty: string | null;
  selectedColorProperty: string | null;
}

export interface ElectionDataState {
  features: PrecinctItem[];
}

interface State {
  controls: ElectionControlsState;
  data: ElectionDataState;
}

const state: State = {
  controls: {
    properties: [],
    selectedYear: null,
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
      .get(`${API_URL}/api/election/precincts`, {
        timeout: 50000,
      })
      .then((res) => {
        commit("updateShowLoadingOverlay", false, { root: true });
        commit("updateFullParcels", JSON.parse(res.data));
      });
  },
};

const mutations = {
  updateFullParcels(state: State, payload: PrecinctItem[]) {
    state.data.features = payload;
    if (payload.length > 0) {
      // Filter to just presidential properties
      const properties = Object.keys(payload[0].properties).filter(
        (el: string) => {
          el.includes("usprs") || el == "2012-2016" || el == "2016-2020";
        }
      );
      state.controls.properties = properties;
      state.controls.selectedYear = 2020;
      state.controls.selectedColorProperty = "2016-2020";
    }
  },
  updateColorProperty(state: State, payload: string) {
    state.controls.selectedColorProperty = payload;
  },
  updateYear(state: State, payload: number) {
    state.controls.selectedYear = payload;
  },
};

const getters = {
  features: (state: State) => {
    return state.data.features;
  },
  properties: (state: State) => {
    return state.controls.properties;
  },
  selectedYear: (state: State) => {
    return state.controls.selectedYear;
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
