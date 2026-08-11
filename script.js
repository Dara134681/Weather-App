// Teaching Tip: Explain 'async' using the waiter/restaurant analogy (Wait for the waiter to return)
async function getWeather() {
    // 1. Get the city the student typed
    const city = document.getElementById("city").value;
    const resultDiv = document.getElementById("result");

    // instructor Checkpoint: This is where we verify the student spelled 'city' correctly.
    if (!city) {
        showMessagePara("Please type a city name.");
        return;
    }

    // Instructor setup: This is the free API Key
    const apiKey = "638ed8715b83a4ab1a9b255417142f33";

    // 2. Build the API 'order' (the URL)
    // Instructor Checkpoint (Image_9.png logic): We must use ${apiKey}, NOT ${city} for appid.
    // Dynamic Variable Fix: city must be enclosed in ${} correctly.
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    // Teaching Concept: The "try...catch" statement prevents the app from crashing.
    try {
        // 3. 'Fetch' the data from the kitchen (OpenWeatherMap server)
        const response = await fetch(url);
        
        // instructor checkpoint (Image_9.png logic): Check if the waiter (response) brought back success.
        if (!response.ok) {
            // A 404 means the city wasn't found, so we throw a clean error.
            throw new Error(`We couldn't find '${city}'. Please check your spelling.`);
        }

        // 4. Open the JSON takeaway box (Wait for the data)
        const data = await response.json();

        // 5. Dynamic DOM Update: Put the food (data) onto the 'plate' (the #result div)
        // Accessing Nested JSON: data.sys.country and data.weather[0] (Image_8.png checkpoint)
        resultDiv.innerHTML = `
            <h3>${data.name}, ${data.sys.country}</h3>
            <p><strong>Temperature:</strong> ${Math.round(data.main.temp)} °C</p>
            <p><strong>Weather:</strong> ${data.weather[0].description}</p>
            <p><strong>Humidity:</strong> ${data.main.humidity}%</p>
        `;
        resultDiv.classList.remove('hidden'); // Show the plate

    } catch (error) {
        // instructor Checkpoint: This is where we catch any network/data errors.
        console.log("Calculations aren't working/screen is empty:", error);
        // Display the specific message defined in throw new Error()
        showMessagePara(`Error: ${error.message}`);
    }
}

// Simple helper function to clear the DOM and show a message
function showMessagePara(text) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<p class="error-message">${text}</p>`;
    resultDiv.classList.remove('hidden');
}

// Optional UX bonus for classroom: Allow pressing 'Enter' to search
// Students must verify the ID "city" exactly.
document.getElementById('city').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        getWeather(); // Manually trigger the function
    }
});