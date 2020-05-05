export interface RootState {
  address: string;
  addressSubmitted: boolean;
}

const rootState: RootState = {
  address: "",
  addressSubmitted: false
};

export default rootState;
