import { GeoJSON } from "leaflet";
import { State as ParcelState } from "./modules/parcels";
import { State as ElectionState } from "./modules/election";
export type LocationDataItem = [number, number, number];

export interface HistDataItem extends Record<string, number | string> {
  YEAR_BUILT: number;
  USECLASS1: string;
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

export interface GrowthItemPoint {
  USECLASS1: string;
  YEAR_BUILT: number;
  Total: number;
  New: number;
  Rates: number;
}

export interface GrowthItem {
  id: string;
  points: GrowthItemPoint[];
}

export type FeatureItem = GeoJSON.Feature<GeoJSON.Polygon, HistDataItem>;

export interface PlotDataState {
  locationData: LocationDataItem[];
  histData: HistDataItem[];
  yearData: Record<number, number>;
  weightData: WeightDataItem[];
  features: FeatureItem[];
  useClasses: string[];
  growthData: GrowthItem[];
  counties: GeoJSON.FeatureCollection<GeoJSON.Polygon, any> | null;
}

export interface UIState {
  showLoadingOverlay: boolean;
}

export type MapTypes = "parcels" | "points";
export interface PlotControlsState {
  selectedUseClasses: string[];
  mapType: MapTypes;
  startYear: number;
  endYear: number;
  analysisRange: number;
  latLng: [null, null] | [number, number];
}

export interface ComputedPlotDataState {
  selectedLocationData: LocationDataItem[];
  selectedHistData: HistDataItem[];
}

export interface RootStateType {
  address: string;
  addressInfo: HereAddress;
  parcels?: ParcelState;
  election?: ElectionState;
  plotControls: PlotControlsState;
  plotData: PlotDataState;
  computedPlotData: ComputedPlotDataState;
  ui: UIState;
}

const genRootState = (): RootStateType => ({
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
    selectedUseClasses: [],
    mapType: "points",
    startYear: 2010,
    endYear: 2020,
    analysisRange: 5000,
    latLng: [null, null],
  },
  computedPlotData: {
    selectedLocationData: [],
    selectedHistData: [],
  },
  plotData: {
    locationData: [],
    histData: [],
    yearData: {},
    weightData: [],
    features: [],
    useClasses: [],
    growthData: [],
    counties: null,
  },
  ui: {
    showLoadingOverlay: false,
  },
});
export { genRootState };
export default genRootState();
