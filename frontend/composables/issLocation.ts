
//
// Composable to fetch ISS position
//
// @param      latitude   The Shared State to be used to return the latitude
// @param      longitude   The Shared State to be used to return the longitude
// @param      timestamp   The Shared State to be used to return the timestamp
// @return     Dictionary:  The shared states with the values from the results of the API call
//
export async function fetchIssLocation(latitude, longitude, timestamp) {
    const config = useRuntimeConfig();

  try {
    const { data, error } = await useFetch(`${config.public.apiBaseUrl}iss/position`);

    if (error.value) {
      console.error('Failed to fetch ISS position:', error.value);
    }
    latitude.value = data.value.latitude
    longitude.value = data.value.longitude
    timestamp.value = data.value.timestamp
    
  } catch (e) {
    console.error('Error fetching ISS position:', e);
  }
  return {  'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp}

  
};