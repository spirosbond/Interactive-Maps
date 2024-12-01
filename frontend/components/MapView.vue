<template>
  <div id="map" class="flex-1 h-full"></div>
  <div class="absolute bg-white rounded-lg shadow-md px-2 py-2 text-sm text-gray-800 border border-gray-200 " ref="popupContainer">
    <p>{{ popupContent }}</p>
  </div>
</template>

<script setup lang="ts">
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { Style, Icon } from 'ol/style';
import iss from '~/assets/img/iss.png';
import Overlay from 'ol/Overlay';

// Configuration for API URL
const config = useRuntimeConfig();

// Popup and coordinates
const popupContainer = useState('popupContainer', () => null)
const popupContent = useState('popupContent', () => "Loading...")
// const latitude = ref(0);
const latitude = useState('latitude', () => 0);
const longitude = useState('longitude', () => 0);
const timestamp = useState('timestamp', () => 0);
fetchLocation(latitude, longitude, timestamp);

// Track whether it's the first update
let firstLoad = true;

// Fetch location initially and then every 20 seconds
onMounted(() => {
  setInterval(() => {
    fetchLocation(latitude, longitude, timestamp);
  }, 20000);

  // Create map view
  const view = new View({
    center: fromLonLat([longitude.value, latitude.value]),
    zoom: 2,
  });

  // Create the map
  const map = new Map({
    target: 'map',
    layers: [
      new TileLayer({
        source: new OSM(),
      }),
    ],
    view: view,
    controls: [],
  });

  // Create a marker feature
  const marker = new Feature({
    geometry: new Point(fromLonLat([longitude.value, latitude.value])),
  });

  // Add a style to the marker
  marker.setStyle(
    new Style({
      image: new Icon({
        src: iss, // Marker icon
        scale: 0.2, // Adjust size
      }),
    })
  );

  // Create a vector source and layer for the marker
  const markerSource = new VectorSource({
    features: [marker],
  });

  const markerLayer = new VectorLayer({
    source: markerSource,
  });

  // Add the marker layer to the map
  map.addLayer(markerLayer);

  // Create the popup overlay
  const popupOverlay = new Overlay({
    element: popupContainer.value,
    positioning: 'bottom-center',
    stopEvent: false,
    offset: [-50, -100],
  });

  map.addOverlay(popupOverlay);

  // Watch for coordinate changes
  watchEffect(() => {
    // Update marker position
    marker.setGeometry(new Point(fromLonLat([longitude.value, latitude.value])));
    popupContent.value = new Date(timestamp.value).toLocaleString();

    // Animate the map to the new center on first load
    if (firstLoad && latitude.value !== 0 && longitude.value !== 0) {
      setTimeout(() => {
      view.animate({
            center: fromLonLat([longitude.value, latitude.value]),
            duration: 400, // 1-second animation
          });
        }, 0); // Delay animation to allow the marker to render first
      firstLoad = false;
    }
  });

  // Add a click event to display the popup when the marker is clicked
  map.on('singleclick', (event) => {
    map.forEachFeatureAtPixel(event.pixel, (feature) => {
      if (feature === marker) {
        const coordinates = (feature.getGeometry() as Point).getCoordinates();
        popupOverlay.setPosition(coordinates);
      }
    });
  });

  // Hide the popup when clicking elsewhere
  map.on('click', (event) => {
    if (!map.hasFeatureAtPixel(event.pixel)) {
      popupOverlay.setPosition(undefined);
    }
  });
});
</script>

<style scoped>
/* Ensure map container occupies full height */
#map {
  height: 100%;
  margin: 0;
}
</style>
