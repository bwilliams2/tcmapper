<template>
  <v-row :style="{ height: '100%' }">
    <v-col sm="12" md="6">
      <NewMap />
    </v-col>
    <v-col sm="12" md="6"> Other plots </v-col>
  </v-row>
</template>

<script>
import Vue from "vue";
import { mapState } from "vuex";
import NewMap from "./NewMap";

export default Vue.extend({
  name: "Home",
  components: {
    NewMap,
  },
});
</script>
