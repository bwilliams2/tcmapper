import { Commit } from "vuex/types";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface PrecinctProperties extends Record<string, unknown> {
  year: number;
}

export type PrecinctItem = GeoJSON.Feature<GeoJSON.Polygon, PrecinctProperties>;
export interface ElectionControlsState {
  properties: string[];
  years: number[];
  selectedYear: number | null;
  selectedPatternProperty: string | null;
  selectedColorProperty: string | null;
}

export interface ElectionDataState {
  features: PrecinctItem[];
  data: Record<string, string | number | null>[];
}

interface State {
  metroControls: ElectionControlsState;
  stateControls: ElectionControlsState;
  data: ElectionDataState;
}

const state: State = {
  metroControls: {
    properties: [],
    years: [],
    selectedYear: 2020,
    selectedPatternProperty: null,
    selectedColorProperty: null,
  },
  stateControls: {
    properties: [],
    years: [],
    selectedYear: 2020,
    selectedPatternProperty: null,
    selectedColorProperty: null,
  },
  data: {
    features: [],
    data: [],
  },
};

const actions = {
  async updateParcels({ commit, state }: { commit: Commit; state: State }) {
    commit("updateShowLoadingOverlay", true, { root: true });
    return axios
      .get(`${API_URL}/api/election/precincts`, {
        params: { year: state.metroControls.selectedYear },
        timeout: 50000,
      })
      .then((res) => {
        commit("updateShowLoadingOverlay", false, { root: true });
        commit("updateFullParcels", JSON.parse(res.data.features));
        commit("updateFullData", JSON.parse(res.data.data));
      });
  },
  updateColorProperty(
    { commit, state }: { commit: Commit; state: State },
    newValue: string
  ) {
    commit("updateColorProperty", newValue);
  },
};

const mutations = {
  updateFullParcels(state: State, payload: PrecinctItem[]) {
    state.data.features = payload;
    const newControls = { ...state.stateControls };
    if (payload.length > 0) {
      // Filter to just presidential properties
      // const properties = Object.keys(payload[0].properties).filter(
      //   (el: string) => {
      //     el.includes("usprs") || el == "2012-2016" || el == "2016-2020";
      //   }
      // );
      const properties = Object.keys(payload[0].properties);
      newControls.properties = [...properties];
      newControls.years = [2012, 2014, 2016, 2018, 2020];
      newControls.selectedYear = 2020;
      newControls.selectedColorProperty = "2020-2016";
      state.stateControls = { ...newControls };
      state.metroControls = { ...newControls };
    }
  },
  updateFullData(state: State, payload: ElectionDataState["data"]) {
    state.data.data = payload;
  },
  updateColorProperty(state: State, payload: string) {
    state.stateControls.selectedColorProperty = payload;
  },
  updateYear(state: State, payload: number) {
    state.stateControls.selectedYear = payload;
  },
  updateMetroColorProperty(state: State, payload: string) {
    state.metroControls.selectedColorProperty = payload;
  },
  updateMetroYear(state: State, payload: number) {
    state.metroControls.selectedYear = payload;
  },
};

const getters = {
  features: (state: State) => {
    return state.data.features;
  },
  properties: (state: State) => {
    return state.stateControls.properties;
  },
  selectedYear: (state: State) => {
    return state.stateControls.selectedYear;
  },
  selectedColorProperty: (state: State) => {
    return state.stateControls.selectedColorProperty;
  },
  selectedPatternProperty: (state: State) => {
    return state.stateControls.selectedPatternProperty;
  },
  selectedMetroYear: (state: State) => {
    return state.metroControls.selectedYear;
  },
  selectedMetroColorProperty: (state: State) => {
    return state.metroControls.selectedColorProperty;
  },
  selectedMetroPatternProperty: (state: State) => {
    return state.metroControls.selectedPatternProperty;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
