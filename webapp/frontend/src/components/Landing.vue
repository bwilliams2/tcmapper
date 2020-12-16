<template>
  <v-container style="height: 100%">
    <v-row justify="center" align="center" style="height: 100%">
      <v-col cols="8" md="10">
        <v-card>
          <v-card-text>
            <v-autocomplete
              v-model="address"
              :items="items"
              :loading="isLoading"
              :search-input.sync="search"
              filled
            ></v-autocomplete>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn class="mr-5" @click.native="submitAddress()"
                >Find My House</v-btn
              >
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";
import _ from "lodash";
const apiKey = process.env.VUE_APP_HERE_API_KEY as string;

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
    lat: number;
    lng: number;
  };
  access: [
    {
      lat: number;
      lng: number;
    }
  ];
  distance: number;
}

interface LandingData {
  isLoading: boolean;
  search: string | null;
  entries: HereAddress[];
  descriptionLimit: number;
}

export default Vue.extend({
  name: "Landing",
  data: (): LandingData => ({
    isLoading: false,
    search: null,
    entries: [],
    descriptionLimit: 60,
  }),
  // created() {
  //   this.updateSearch = debounce(this.updateSearch, 300);
  // },
  // mounted() {
  //   this.sessionToken = uuidv4();
  // },
  computed: {
    items(): string[] {
      return this.entries.map((e) => e.title);
    },
    address: {
      get() {
        return this.$store.state.address;
      },
      set(value) {
        return this.$store.commit("updateAddress", { address: value });
      },
    },
    ...mapState(["addressInfo"]),
  },
  methods: {
    submitAddress() {
      // Instantiate a map and platform object:
      const platform = new window.H.service.Platform({
        apikey: apiKey,
      });
      // Get an instance of the search service:
      const service = platform.getSearchService();

      service.autosuggest(
        {
          // Search query
          q: this.address,
          // Center of the search context
          in: "circle:44.985207,-93.264622;r=50000",
          // at: "44.985207,-93.264622"
        },
        (result: any) => {
          const addressInfo = _.pick(
            result.items[0],
            ...Object.keys(this.addressInfo)
          );
          this.$store.dispatch("updateAddressInfo", addressInfo).then(() => {
            this.$router.push({ path: "/map" });
          });
          // Assumption: ui is instantiated
          // Create an InfoBubble at the returned location
          // ui.addBubble(new H.ui.InfoBubble(position, {
          //   content: title
          // }));
        },
        alert
      );
    },
    updateAddress(e: Event) {
      if (e?.target) {
        const target = e.target as HTMLInputElement;
        this.$store.dispatch("updateAddress", target.value);
      }
    },
  },
  watch: {
    search(val) {
      // Items have already been loaded
      // if (this.items.length > 0) return;
      if (val === "") {
        return;
      }

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Instantiate a map and platform object:
      const platform = new window.H.service.Platform({
        apikey: apiKey,
      });
      // Get an instance of the search service:
      const service = platform.getSearchService();

      // Call the "autosuggest" method with the search parameters,
      // the callback and an error callback function (called if a
      // communication error occurs):
      const changeLoading = () => {
        this.isLoading = false;
      };
      service.autosuggest(
        {
          // Search query
          q: val,
          // Center of the search context
          in: "circle:44.985207,-93.264622;r=50000",
          // at: "44.985207,-93.264622"
        },
        (result: any) => {
          this.entries = result.items;
          changeLoading();
          // Assumption: ui is instantiated
          // Create an InfoBubble at the returned location
          // ui.addBubble(new H.ui.InfoBubble(position, {
          //   content: title
          // }));
        },
        alert
      );
    },
  },
});
</script>
