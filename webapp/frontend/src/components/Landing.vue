<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="6">
        <v-card-text>
          Enter base address
        </v-card-text>
        <v-card-text>
          <v-autocomplete
            :value="address"
            @input="updateAddress"
            :items="items"
            :loading="isLoading"
            :search-input.sync="search"
            filled
          ></v-autocomplete>
        </v-card-text>
        <v-btn class="mr-5">Find My House</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import hereInit from "../utils/here";
const apiKey = process.env.HERE_API_KEY as string;

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
    descriptionLimit: 60
  }),
  // mounted() {
  //   this.sessionToken = uuidv4();
  // },
  computed: {
    items(): string[] {
      return this.entries.map(e => e.title);
    },
    ...mapState(["address"])
  },
  methods: {
    updateAddress(e: Event) {
      if (e?.target) {
        const target = e.target as HTMLInputElement;
        this.$store.commit("updateAddress", target.value);
      }
    }
  },
  watch: {
    async search(val) {
      const H = (await hereInit()) as any;

      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Instantiate a map and platform object:
      const platform = new H.service.Platform({
        apikey: apiKey
      });
      // Get an instance of the search service:
      const service = platform.getSearchService();

      // Call the "autosuggest" method with the search parameters,
      // the callback and an error callback function (called if a
      // communication error occurs):
      service.autosuggest(
        {
          // Search query
          q: val,
          // Center of the search context
          in: "circle:44.985207,-93.264622;r=50000"
        },
        (result: any) => {
          const { position, title } = result.items[0];
          // Assumption: ui is instantiated
          // Create an InfoBubble at the returned location
          // ui.addBubble(new H.ui.InfoBubble(position, {
          //   content: title
          // }));
        },
        alert
      );

      // Lazily load input items
      // axios.get(
      //   'https://autosuggest.search.hereapi.com/v1/autosuggest',
      //   { params: { q: val, in: "circle:44.985207,-93.264622;r=50000", apiKey: apiKey } },
      // )
      //   .then(res => {
      //     const d =0;
      //     this.entries = res.data;
      //  })
      // .catch(err => {
      //   console.log(err)
      // })
      // .finally(() => (this.isLoading = false))
    }
  }
});
</script>
