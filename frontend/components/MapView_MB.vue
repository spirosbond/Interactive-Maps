 <template>
  <div id="map" class="flex-1"></div>

</template>

<script setup lang="ts">
// import { defineComponent, onMounted } from 'vue';
import mapboxgl from 'mapbox-gl';
// import { useRuntimeConfig } from '#app';
// export default defineNuxtComponent({
  // name: 'MapView_MB',
  // setup() {
    // const iss_location = issLocation();
    const {data, error} = await useFetch('https://inter-maps-backend-974996545024.europe-west1.run.app/api/iss/position')
    console.log(data.value.longitude)
    const config = useRuntimeConfig();
    // Lifecycle hook to initialize the map
    onMounted(() => {
      initMap();
    });

    // Function to initialize the Mapbox map
    const initMap = () => {
      
      // Set the Mapbox access token from runtime config
      mapboxgl.accessToken = config.public.mapboxToken;

      // Initialize the Mapbox map
      const map = new mapboxgl.Map({
        container: 'map', // ID of the div to contain the map
        style: 'mapbox://styles/mapbox/streets-v11', // Mapbox style
        center: [2.3522, 48.8566], // Coordinates for the map's center [longitude, latitude]
        zoom: 2, // Zoom level
        attributionControl: false, // Disable attribution control if needed
      });
      // Add a marker at the ISS location
        // const marker = new mapboxgl.Marker().setLngLat([data.value.longitude, data.value.latitude]).addTo(map);
        const marker = new mapboxgl.Marker().setLngLat([2.3522, 48.8566]).addTo(map);

    };

    // return {};
  // },
// });
</script>

<style scoped>
#map {
  height: 100%;
  width: 100%;
}
</style>
