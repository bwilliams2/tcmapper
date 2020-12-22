export type LocationDataItem = [number, number, number];

export interface HistDataItem extends Record<string, number> {
  YEAR_BUILT: number;
}

export interface YearDataItem {
  YEAR_BUILT: number;
  COUNT: number;
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

export interface PlotDataState {
  locationData: LocationDataItem[];
  histData: HistDataItem[];
  yearData: YearDataItem[];
  weightData: WeightDataItem[];
  analysisDistance: number | null;
}

export interface UIState {
  showLoadingOverlay: boolean;
}

export interface PlotControlsState {
  startYear: number;
  endYear: number;
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
    startYear: 2010,
    endYear: 2020,
  },
  plotData: {
    locationData: [],
    histData: [],
    yearData: [],
    weightData: [],
    analysisDistance: 5000,
  },
  ui: {
    showLoadingOverlay: false,
  },
};

export default rootState;
