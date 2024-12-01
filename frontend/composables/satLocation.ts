
//
// Composable to fetch the location of a satellite
//
// @param      sat_id      The id of the satellite
// @param      locations   The Shared State to be used to return the locations
// @return     locations:  The Shared State with the results of the API call
//
export async function fetchSatLocations(sat_id, n, locations) {
  const config = useRuntimeConfig();
  const toast = useToast()

  try {
    const { data, error } = await useFetch(`${config.public.apiBaseUrl}location/by_sat_id/${sat_id}?limit=${n}`);
    if (error.value) {
      console.error('Failed to fetch ISS position:', error.value);
    }
    locations.value = data.value.locations

  } catch (e) {
    console.error('Error fetching ISS position:', e);
    toast.add({
        id: 'fetch_error',
        color: "red",
        title: 'Error Fetching Satellite location!',
        timeout: 5000,
        actions: [{
          label: 'Reload Page',
          click: () => {
            reloadNuxtApp({"ttl":1})
          }
        }]
    })
  }
  return locations

  
};