// index.js

// --- Fetch Weather ---
async function loadWeather(city = "New York") {
    const apiKey = OPENWEATHER_API_KEY.weather; // Use the key from the global object
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        const weatherEl = document.querySelector("#weather");
        if (weatherEl && data.cod === 200) {
            const temp = data.main.temp;
            const desc = data.weather[0].description;
            const wind = data.wind.speed;
            const humidity = data.main.humidity;

            weatherEl.innerHTML = `
                <strong>${data.name}</strong>: ${temp}°C, ${desc}<br>
                💨 Wind: ${wind} m/s<br>
                💧 Humidity: ${humidity}%
            `;
        } else if (weatherEl) {
            weatherEl.textContent = "City not found!";
        }
    } catch (err) {
        console.error("Weather fetch error:", err);
        const weatherEl = document.querySelector("#weather");
        if (weatherEl) weatherEl.textContent = "Weather data unavailable";
    }
}

// --- Fetch Trending News ---
async function loadTrendingNews() {
    const apiKey = NEWS_API_KEY.news; // Use the key from the global object
    const url = `https://newsapi.org/v2/top-headlines?country=us&pageSize=3&apiKey=${apiKey}`;

    try {
        const res = await fetch(url);
        const data = await res.json();
        const newsList = document.querySelector("#trending-news");
        if (newsList) {
            newsList.innerHTML = "";
            if (data.articles && data.articles.length > 0) {
                data.articles.forEach(article => {
                    const li = document.createElement("li");
                    li.textContent = article.title;
                    newsList.appendChild(li);
                });
            } else {
                newsList.innerHTML = "<li>No news available</li>";
            }
        }
    } catch (err) {
        console.error("News fetch error:", err);
        const newsList = document.querySelector("#trending-news");
        if (newsList) newsList.innerHTML = "<li>Unable to load news</li>";
    }
}

// --- Animated Counters ---
function runCounters() {
    document.querySelectorAll(".counter").forEach((counter) => {
        const target = parseFloat(counter.getAttribute("data-target"));
        let count = 0;
        const increment = Math.max(target / 100, 1);

        const updateCounter = () => {
            if (count < target) {
                count += increment;
                if (Number.isInteger(target)) {
                    counter.innerText = Math.min(Math.ceil(count), target);
                } else {
                    counter.innerText = Math.min(count, target).toFixed(1);
                }
                setTimeout(updateCounter, 20);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });
}

// --- Init ---
document.addEventListener("DOMContentLoaded", () => {
    // Load default weather
    loadWeather();
    loadTrendingNews();
    runCounters();

    // Listen for city search
    const cityForm = document.querySelector("#city-form");
    if (cityForm) {
        cityForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const cityInput = document.querySelector("#city-input");
            if (cityInput && cityInput.value.trim() !== "") {
                loadWeather(cityInput.value.trim());
                cityInput.value = "";
            }
        });
    }
});