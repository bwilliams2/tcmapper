const CALLBACK_NAME = "hereCallback";

declare global {
  interface Window {
    here: any;
    hereCallback: any;
  }
}

let initialized = !!window.here;
let resolveInitPromise: (value?: any | PromiseLike<any>) => void;
let rejectInitPromise: (reason?: any) => void;
// This promise handles the initialization
// status of the google maps script.
const initPromise = new Promise((resolve, reject) => {
  resolveInitPromise = resolve;
  rejectInitPromise = reject;
});

export default function init() {
  // If Google Maps already is initialized
  // the `initPromise` should get resolved
  // eventually.
  if (initialized) return initPromise;

  initialized = true;
  // The callback function is called by
  // the Google Maps script if it is
  // successfully loaded.
  window[CALLBACK_NAME] = () => resolveInitPromise(window.here);

  // We inject a new script tag into
  // the `<head>` of our HTML to load
  // the Google Maps script.
  const script = document.createElement("script");
  script.async = true;
  script.defer = true;
  script.src = `https://js.api.here.com/v3/3.1/mapsjs-core.js`;
  script.type = "text/javascript";
  script.charset = "utf-8";
  script.onerror = rejectInitPromise;
  document.querySelector("head")?.appendChild(script);

  return initPromise;
}
