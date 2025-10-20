const API_URL = "https://echosense-2.onrender.com/api";

// -----------------------------
// Check Login Token
// -----------------------------
const token = localStorage.getItem("token");
if (!token && !window.location.href.includes("login") && !window.location.href.includes("signup")) {
    window.location.href = "login.html";
}

// -----------------------------
// Logout Function
// -----------------------------
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        window.location.href = "login.html";
    });
}

// -----------------------------
// Voice Recorder Utility
// -----------------------------
async function recordVoice(micBtn, inputBox) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        mediaRecorder.ondataavailable = e => chunks.push(e.data);
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(chunks, { type: "audio/webm" });
            const formData = new FormData();
            formData.append("file", audioBlob, "audio.webm");

            try {
                const res = await fetch(`${API_URL}/speech-to-text`, {
                    method: "POST",
                    headers: { "Authorization": `Bearer ${token}` },
                    body: formData,
                });
                const data = await res.json();
                inputBox.value = data.text || "";
            } catch (err) {
                console.error("Voice-to-text error:", err);
                alert("Error processing audio. Try again.");
            }

            micBtn.classList.remove("active");
        };

        mediaRecorder.start();
        micBtn.classList.add("active");
        setTimeout(() => mediaRecorder.stop(), 6000); // 6 seconds recording
    } catch (err) {
        console.error("Microphone access error:", err);
        alert("Cannot access microphone. Check permissions.");
    }
}

// -----------------------------
// Diary + Chat Elements
// -----------------------------
const diaryInput = document.getElementById("diary-input");
const diaryMic = document.getElementById("mic-diary");
const saveDiary = document.getElementById("save-diary");
const diaryResponseDiv = document.getElementById("diary-response");

const chatInput = document.getElementById("chat-input");
const chatMic = document.getElementById("mic-chat");
const sendChat = document.getElementById("send-chat");
const chatBox = document.getElementById("chat-box");

if(diaryMic) diaryMic.addEventListener("click", () => recordVoice(diaryMic, diaryInput));
if(chatMic) chatMic.addEventListener("click", () => recordVoice(chatMic, chatInput));

// -----------------------------
// Diary Save + AI Response
// -----------------------------
if(saveDiary) saveDiary.addEventListener("click", async () => {
    const message = diaryInput.value.trim();
    if (!message) return;

    diaryResponseDiv.innerHTML = "<p>Saving diary and analyzing mood...</p>";

    try {
        const res = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ user_message: message, diary: true })
        });
        const data = await res.json();

        diaryResponseDiv.innerHTML = `
            <div class="chat-message diary-user">📝 You: ${data.user_message}</div>
            <div class="chat-message diary-bot">🤖 EchoSense: ${data.bot_response}</div>
        `;

        const mood = (data.mood || "neutral").toLowerCase();
        let color = "#f5f5f5";
        if (mood === "happy") color = "#fff3b0";
        else if (mood === "sad") color = "#d0e1f9";

        diaryInput.style.backgroundColor = color;
        diaryResponseDiv.style.backgroundColor = color;
        diaryInput.value = "";
        diaryResponseDiv.scrollTop = diaryResponseDiv.scrollHeight;

    } catch (err) {
        diaryResponseDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
});

// -----------------------------
// Chat System
// -----------------------------
if(sendChat) sendChat.addEventListener("click", async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    chatBox.innerHTML += `<div class="chat-message user">${message}</div>`;
    chatInput.value = "";

    try {
        const res = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ user_message: message })
        });

        const data = await res.json();
        chatBox.innerHTML += `<div class="chat-message bot">${data.bot_response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch(err) {
        console.error("Chat error:", err);
        chatBox.innerHTML += `<div class="chat-message bot" style="color:red;">Error: Could not reach server.</div>`;
    }
});

// -----------------------------
// Mood Board Navigation
// -----------------------------
const viewMoodBtn = document.getElementById("view-mood-board");
if(viewMoodBtn) viewMoodBtn.addEventListener("click", () => {
    window.location.href = "mood-board.html";
});

// -----------------------------
// Mood Board Loading
// -----------------------------
const loadBtn = document.getElementById("loadMood");
const periodSelect = document.getElementById("period");
const moodText = document.getElementById("mood-text-summary");
let moodChart;

async function loadMoodBoard() {
    if(!loadBtn) return;
    const period = periodSelect.value;

    const res = await fetch(`${API_URL}/mood-board?period=${period}`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();

    const labels = Object.keys(data.summary);
    const happy = labels.map(k => data.summary[k].happy);
    const sad = labels.map(k => data.summary[k].sad);
    const neutral = labels.map(k => data.summary[k].neutral);

    if (moodChart) moodChart.destroy();
    const ctx = document.getElementById("moodChart").getContext("2d");
    moodChart = new Chart(ctx, {
        type: "bar",
        data: { labels, datasets: [
            { label: "Happy 😊", data: happy, backgroundColor: "rgba(75,192,192,0.6)" },
            { label: "Sad 😢", data: sad, backgroundColor: "rgba(255,99,132,0.6)" },
            { label: "Neutral 😐", data: neutral, backgroundColor: "rgba(201,203,207,0.6)" }
        ]},
        options: {
            responsive: true,
            animation: { duration: 1200, easing: 'easeOutQuart' },
            plugins: { title: { display: true, text: `Mood Summary (${period})`, font: { size: 20 } } },
            scales: { y: { beginAtZero: true } }
        }
    });

    // Display last 10 moods and quote
    moodText.innerHTML = `
        <p>📝 <strong>Last 10 entries:</strong> ${data.last_10_moods.join(", ")}</p>
        <p>🌟 <strong>Dominant mood:</strong> ${data.dominant_mood}</p>
        <p>💬 <strong>Motivational quote:</strong> ${data.quote}</p>
    `;
}

if(loadBtn) loadBtn.addEventListener("click", loadMoodBoard);
window.addEventListener("load", loadMoodBoard);

// -----------------------------
// Back Button
// -----------------------------
const backBtn = document.getElementById("back-home");
if(backBtn) backBtn.addEventListener("click", () => window.location.href = "profile.html");
