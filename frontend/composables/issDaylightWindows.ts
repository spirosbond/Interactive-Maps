
//
// Composable to fetch ISS windows under the sun
//
// @param      timeWindows:  The Shared State to be used to return the windows from the API
// @return     timeWindows:  The daylight windows.
//
export async function fetchDaylightWindows() {
  const config = useRuntimeConfig();
  const toast = useToast()
  const timeWindows = useState("timeWindows", () => "Loading...");

  try {
    const { data, error } = await useFetch(`${config.public.apiBaseUrl}iss/sun`);
    
    if (error.value) {
      console.error('Failed to fetch ISS Daylight Windows:', error.value);
    }
    timeWindows.value = data.value.windows
    
  } catch (e) {
    console.error('Error fetching ISS Daylight Windows:', e);
    toast.add({
        id: 'fetch_error',
        color: "red",
        title: 'Error Fetching ISS Daylight Windows!',
        timeout: 5000,
        actions: [{
          label: 'Reload Page',
          click: () => {
            reloadNuxtApp({"ttl":1})
          }
        }]
    })
  }
  return timeWindows

  
};