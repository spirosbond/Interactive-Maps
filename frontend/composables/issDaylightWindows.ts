
//
// Composable to fetch ISS windows under the sun
//
// @param      windows:  The Shared State to be used to return the windows from the API
// @return     windows:  The daylight windows.
//
export async function fetchDaylightWindows(windows) {
    const config = useRuntimeConfig();
    
  try {
    const { data, error } = await useFetch(config.public.apiBaseUrl + 'iss/sun');
    
    if (error.value) {
      console.error('Failed to fetch ISS Daylight Windows:', error.value);
    }
    windows.value = data.value.windows
    
  } catch (e) {
    console.error('Error fetching ISS position:', e);
  }
  return windows

  
};