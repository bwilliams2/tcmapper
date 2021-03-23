import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Landing from "@/components/landing/Landing.vue";
import MapData from "@/components/mapplot/MapData.vue";
import ElectionState from "@/components/electionState/ElectionState.vue";
import ElectionMetro from "@/components/electionMetro/ElectionMetro.vue";
import Base from "@/components/base/Base.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    component: Home,
    children: [
      { path: "", component: Base, name: "home" },
      { path: "/parcels", component: Landing, name: "parcels" },
      { path: "/parcels/stats", component: MapData, name: "densityMap" },
      {
        path: "/election/stateprecincts",
        component: ElectionState,
        name: "electionState",
      },
      {
        path: "/election/metromodel",
        component: ElectionMetro,
        name: "electionMetro",
      },
      // { path: "", component: MapData, name: "home" },
    ],
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.VUE_ROUTER_BASE,
  routes,
});

export default router;
