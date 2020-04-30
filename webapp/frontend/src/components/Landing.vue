<template>
  <v-container fluid>
    <v-col cols="12">
      <v-row
        align="center"
        justify="center"
        class="grey lighten-5"
        style="height: 300px;"
      >
        <v-card v-for="n in 3" :key="n" class="ma-3 pa-6" outlined tile>
          Column
        </v-card>
      </v-row>
    </v-col>
    <!-- <v-row justify="end">
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
        <v-btn>Find My House</v-btn>
      </v-col>
    </v-row> -->
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";

export default Vue.extend({
  name: "Landing",
  data: () => ({
    isLoading: false,
    search: null,
    entries: [],
    descriptionLimit: 60
  }),
  computed: {
    items() {
      return ["6643 Pelican Pl", "600 Blake St"];
    },
    ...mapState(["address"])
  },
  methods: {
    updateAddress(e: Event) {
      if (event?.target) {
        const target = event.target as HTMLInputElement;
        this.$store.commit("updateAddress", target.value);
      }
    }
  },
  watch: {
    search(val) {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      // fetch('https://api.publicapis.org/entries')
      //   .then(res => res.json())
      //   .then(res => {
      //     const { count, entries } = res
      //     this.count = count
      //     this.entries = entries
      //   })
      //   .catch(err => {
      //     console.log(err)
      //   })
      //   .finally(() => (this.isLoading = false))
      // },
    }
  }
});
</script>
