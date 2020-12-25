import { GeoJSON } from "leaflet";

export type LocationDataItem = [number, number, number];

export interface HistDataItem extends Record<string, number> {
  YEAR_BUILT: number;
}

export interface WeightDataItem {
  YEAR_BUILT: number;
  WEIGHT: number;
}

export interface HereAddress {
  title: string;
  id: string;
  resultType: string;
  houseNumberType: string;
  address: {
    label: string;
    countryCode: string;
    countryName: string;
    state: string;
    county: string;
    city: string;
    street: string;
    postalCode: string;
    houseNumber: string;
  };
  position: {
    lat: number | null;
    lng: number | null;
  };
  access: [
    {
      lat: number | null;
      lng: number | null;
    }
  ];
}

export type FeatureItem = GeoJSON.Feature<GeoJSON.Polygon, HistDataItem>;

export interface PlotDataState {
  locationData: LocationDataItem[];
  histData: HistDataItem[];
  yearData: Record<number, number>;
  weightData: WeightDataItem[];
  features: FeatureItem[];
}

export interface UIState {
  showLoadingOverlay: boolean;
}

export type MapTypes = "parcels" | "points";
export interface PlotControlsState {
  mapType: MapTypes;
  startYear: number;
  endYear: number;
  analysisRange: number | null;
}

export interface RootStateType {
  address: string;
  addressInfo: HereAddress;
  plotControls: PlotControlsState;
  plotData: PlotDataState;
  ui: UIState;
}

const rootState: RootStateType = {
  address: "",
  addressInfo: {
    title: "",
    id: "",
    resultType: "",
    houseNumberType: "",
    address: {
      label: "",
      countryCode: "",
      countryName: "",
      state: "",
      county: "",
      city: "",
      street: "",
      postalCode: "",
      houseNumber: "",
    },
    position: {
      lat: null,
      lng: null,
    },
    access: [
      {
        lat: null,
        lng: null,
      },
    ],
  },
  plotControls: {
    mapType: "points",
    startYear: 2010,
    endYear: 2020,
    analysisRange: 5000,
  },
  plotData: {
    locationData: [],
    histData: [],
    yearData: {},
    weightData: [],
    features: [],
  },
  ui: {
    showLoadingOverlay: false,
  },
};

export default rootState;
