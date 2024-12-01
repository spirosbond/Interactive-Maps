
//
// Composable to fetch the location of a satellite
//
// @param      sat_id      The id of the satellite
// @param      locations   The Shared State to be used to return the locations
// @return     locations:  The Shared State with the results of the API call
//
export async function fetchSatLocations(sat_id, n, locations) {
    const config = useRuntimeConfig();

  try {
    const { data, error } = await useFetch(config.public.apiBaseUrl + 'location/by_sat_id/' + sat_id + '?limit=' + n);
    if (error.value) {
      console.error('Failed to fetch ISS position:', error.value);
    }
    locations.value = data.value.locations

  } catch (e) {
    console.error('Error fetching ISS position:', e);
  }
  return locations

  
};