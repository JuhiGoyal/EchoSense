const API_URL = "http://127.0.0.1:8000/api";
const loadBtn = document.getElementById("loadMood");
const periodSelect = document.getElementById("period");
const moodText = document.getElementById("mood-text-summary");
const moodQuote = document.getElementById("mood-quote");
const backBtn = document.getElementById("back-home");
const logoutBtn = document.getElementById("logout-btn");

const token = localStorage.getItem("token");
if (!token) window.location.href = "login.html";

let moodChart;

// -----------------------------
// Logout Button
// -----------------------------
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        window.location.href = "login.html";
    });
}

// -----------------------------
// Load Mood Board
// -----------------------------
async function loadMoodBoard() {
    const period = periodSelect.value;

    try {
        const res = await fetch(`${API_URL}/mood-board?period=${period}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        const labels = Object.keys(data.summary);
        const happy = labels.map(k => data.summary[k].happy);
        const sad = labels.map(k => data.summary[k].sad);
        const neutral = labels.map(k => data.summary[k].neutral);

        // Chart
        const ctx = document.getElementById("moodChart").getContext("2d");
        if (moodChart) moodChart.destroy();
        moodChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    { label: "Happy 😊", data: happy, backgroundColor: "rgba(75,192,192,0.6)" },
                    { label: "Sad 😢", data: sad, backgroundColor: "rgba(255,99,132,0.6)" },
                    { label: "Neutral 😐", data: neutral, backgroundColor: "rgba(201,203,207,0.6)" }
                ]
            },
            options: {
                responsive: true,
                animation: { duration: 1200, easing: 'easeOutQuart' },
                plugins: { title: { display: true, text: `Mood Summary (${period.charAt(0).toUpperCase() + period.slice(1)})`, font: { size: 20 } } },
                scales: { y: { beginAtZero: true } }
            }
        });

        // Text summary
        const totalHappy = happy.reduce((a,b)=>a+b,0);
        const totalSad = sad.reduce((a,b)=>a+b,0);
        const totalNeutral = neutral.reduce((a,b)=>a+b,0);
        let dominant = "😐 Neutral";
        if (totalHappy > totalSad && totalHappy > totalNeutral) dominant = "😊 Happy";
        else if (totalSad > totalHappy && totalSad > totalNeutral) dominant = "😢 Sad";

        moodText.innerHTML = `
            <p>📝 <strong>Total entries:</strong> ${totalHappy + totalSad + totalNeutral}</p>
            <p>🌟 <strong>Dominant mood:</strong> ${dominant}</p>
            <p>😊 Happy: ${totalHappy} &nbsp; 😢 Sad: ${totalSad} &nbsp; 😐 Neutral: ${totalNeutral}</p>
        `;

        // Mood-specific quote
        const quote = data.quote || "Keep going, your mood matters!";
        moodQuote.innerHTML = `<p>💬 Quote: "${quote}"</p>`;

    } catch(err) {
        console.error(err);
        alert("Error loading mood board.");
    }
}

// -----------------------------
// Event Listeners
// -----------------------------
if(loadBtn) loadBtn.addEventListener("click", loadMoodBoard);
if(backBtn) backBtn.addEventListener("click", () => window.location.href = "profile.html");

// Auto-load on page load
window.addEventListener("load", loadMoodBoard);
