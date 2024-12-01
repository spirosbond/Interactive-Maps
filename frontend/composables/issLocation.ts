
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
    // Using fetch instead of useState because this Composable runs with an interval on the client
    const data = await $fetch(`${config.public.apiBaseUrl}iss/position`);

    latitude.value = data.latitude
    longitude.value = data.longitude
    timestamp.value = data.timestamp 
    
    
  } catch (e) {
    console.error('Error fetching ISS position:', e);
  }
  return {  latitude,
            longitude,
            timestamp}

  
};