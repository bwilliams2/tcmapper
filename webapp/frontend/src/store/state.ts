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
  distance: number | null;
}

export interface RootState {
  address: string;
  addressInfo: HereAddress;
}

const rootState: RootState = {
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
      houseNumber: ""
    },
    position: {
      lat: null,
      lng: null
    },
    access: [
      {
        lat: null,
        lng: null
      }
    ],
    distance: null
  }
};

export default rootState;
