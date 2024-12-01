
// Function to fetch ISS position
export async function fetchLocation(latitude, longitude, timestamp) {
    const config = useRuntimeConfig();
    // const latitude = ref(0)
    // const longitude = ref(0)
    // const timestamp = ref('Loading...')
  try {
    const { data, error } = await useFetch(config.public.apiBaseUrl + 'iss/position');
    if (error.value) {
      console.error('Failed to fetch ISS position:', error.value);
    }
    latitude.value = data.value.latitude
    longitude.value = data.value.longitude
    timestamp.value = data.value.timestamp

    // Update marker position and timestamp
    // if (data.value) {
      // markerCoordinates.value = [data.value.longitude, data.value.latitude];
      // markerTimestamp.value = new Date(data.value.timestamp).toLocaleString();
    // } else {
      // console.error('Data is null or undefined');
    // }
    // console.log(latitude)
    
  } catch (e) {
    console.error('Error fetching ISS position:', e);
  }
  return {  'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp}

  
};