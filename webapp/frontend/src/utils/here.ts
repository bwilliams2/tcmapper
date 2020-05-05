const CALLBACK_NAME = "hereCallback";

declare global {
  interface Window {
    H: any;
    hereCallback: any;
  }
}

let initialized = !!window.H;
let resolveInitPromise: (value?: any | PromiseLike<any>) => void;
let rejectInitPromise: (reason?: any) => void;
let resolveInitPromise2: (value?: any | PromiseLike<any>) => void;
let rejectInitPromise2: (reason?: any) => void;
// This promise handles the initialization
// status of the google maps script.
const initPromise = new Promise((resolve, reject) => {
  resolveInitPromise = resolve;
  rejectInitPromise = reject;
});

const initPromise2 = new Promise((resolve, reject) => {
  resolveInitPromise2 = resolve;
  rejectInitPromise2 = reject;
});

export default function init() {
  // If Google Maps already is initialized
  // the `initPromise` should get resolved
  // eventually.
  if (initialized) return Promise.all([initPromise, initPromise2]);

  initialized = true;
  // The callback function is called by
  // the Google Maps script if it is
  // successfully loaded.

  // We inject a new script tag into
  // the `<head>` of our HTML to load
  // the Google Maps script.
  const script = document.createElement("script");
  script.src = `https://js.api.here.com/v3/3.1/mapsjs-core.js`;
  script.type = "text/javascript";
  script.charset = "utf-8";
  script.onload = () => resolveInitPromise(window.H.Maps);
  script.onerror = rejectInitPromise;
  document.querySelector("head")?.appendChild(script);

  const script2 = document.createElement("script");
  script2.async = true;
  script2.defer = true;
  script2.src = `https://js.api.here.com/v3/3.1/mapsjs-service.js`;
  script2.type = "text/javascript";
  script2.charset = "utf-8";
  script2.onload = () => resolveInitPromise2(window.H.service);
  script2.onerror = rejectInitPromise2;
  document.querySelector("head")?.appendChild(script2);

  return Promise.all([initPromise, initPromise2]);
}
