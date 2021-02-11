import { Commit } from "vuex/types";
import { API_URL } from "@/utils/misc";
import axios from "axios";

export interface PrecinctProperties extends Record<string, unknown> {
  year: number;
}

export type PrecinctItem = GeoJSON.Feature<GeoJSON.Polygon, PrecinctProperties>;
export interface ElectionControlsState {
  properties: Record<string, string[]>;
  categories: string[];
  years: number[];
  selectedYear: number | null;
  selectedCategory: string | null;
  selectedProperty: string | null;
}

export interface ElectionDataState {
  features: PrecinctItem[];
  data: Record<string, string | number | null>[];
}

export interface State {
  metroControls: ElectionControlsState;
  stateControls: ElectionControlsState;
  data: ElectionDataState;
}

const state: State = {
  metroControls: {
    properties: {},
    categories: [],
    years: [2012, 2014, 2016, 2018, 2020],
    selectedYear: 2020,
    selectedCategory: null,
    selectedProperty: null,
  },
  stateControls: {
    properties: {},
    categories: [],
    years: [2012, 2014, 2016, 2018, 2020],
    selectedYear: 2020,
    selectedCategory: null,
    selectedProperty: null,
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
        const properties = JSON.parse(res.data.selection);
        const categories = Object.keys(properties);
        commit("updateProperties", properties);
        commit("updateCategories", categories);
      });
  },
  updateSelectedCategory(
    { commit, state }: { commit: Commit; state: State },
    newValue: string
  ) {
    commit("updateSelectedCategory", newValue);
    commit("updateSelectedProperty", null);
  },
  updateSelectedProperty(
    { commit, state }: { commit: Commit; state: State },
    newValue: string
  ) {
    commit("updateSelectedProperty", newValue);
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
      newControls.selectedYear = 2020;
      newControls.selectedCategory = "usprs";
      newControls.selectedProperty = "2020-2016";
      state.stateControls = { ...newControls };
      state.metroControls = { ...newControls };
    }
  },
  updateProperties(state: State, payload: Record<string, string[]>) {
    state.stateControls.properties = payload;
    state.metroControls.properties = payload;
  },
  updateCategories(state: State, payload: string[]) {
    state.stateControls.categories = payload;
    state.metroControls.categories = payload;
  },
  updateFullData(state: State, payload: ElectionDataState["data"]) {
    state.data.data = payload;
  },
  updateSelectedProperty(state: State, payload: string) {
    state.stateControls.selectedProperty = payload;
  },
  updateSelectedCategory(state: State, payload: string) {
    state.stateControls.selectedCategory = payload;
  },
  updateYear(state: State, payload: number) {
    state.stateControls.selectedYear = payload;
  },
  updateMetroColorProperty(state: State, payload: string) {
    state.metroControls.selectedProperty = payload;
  },
  updateMetroYear(state: State, payload: number) {
    state.metroControls.selectedYear = payload;
  },
};

const getters = {
  features: (state: State) => {
    return state.data.features;
  },
  years: (state: State) => {
    return state.stateControls.years;
  },
  properties: (state: State) => {
    const category = state.stateControls.selectedCategory;
    if (category) {
      return state.stateControls.properties[category];
    } else {
      return [];
    }
  },
  categories: (state: State) => {
    return state.stateControls.categories;
  },
  selectedYear: (state: State) => {
    return state.stateControls.selectedYear;
  },
  selectedCategory: (state: State) => {
    return state.stateControls.selectedCategory;
  },
  selectedProperty: (state: State) => {
    return state.stateControls.selectedProperty;
  },
  selectedMetroYear: (state: State) => {
    return state.metroControls.selectedYear;
  },
  selectedMetroCategory: (state: State) => {
    return state.metroControls.selectedCategory;
  },
  selectedMetroProperty: (state: State) => {
    return state.metroControls.selectedProperty;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
