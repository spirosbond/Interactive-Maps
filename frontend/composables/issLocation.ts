
//
// Composable to fetch ISS position
//
// @param      latitude   The Shared State to be used to return the latitude
// @param      longitude   The Shared State to be used to return the longitude
// @param      timestamp   The Shared State to be used to return the timestamp
// @return     Dictionary:  The shared states with the values from the results of the API call
//
export async function fetchIssLocation() {
  const config = useRuntimeConfig();
  const toast = useToast()
  const latitude = useState('latitude', () => 0);
  const longitude = useState('longitude', () => 0);
  const timestamp = useState('timestamp', () => 0);

  try {
    // Using fetch instead of useFetch because this Composable runs with an interval on the client
    const data = await $fetch(`${config.public.apiBaseUrl}iss/position`);

    latitude.value = data.latitude
    longitude.value = data.longitude
    timestamp.value = data.timestamp 
    
    
  } catch (e) {
    console.error('Error fetching ISS position:', e);
    toast.add({
        id: 'fetch_error',
        color: "red",
        title: 'Error Fetching ISS location!',
        timeout: 5000,
        actions: [{
          label: 'Reload Page',
          click: () => {
            reloadNuxtApp({"ttl":1})
          }
        }]
    })
  }
  return {  latitude,
            longitude,
            timestamp}

  
};