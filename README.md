# EchoSense 🌟

**EchoSense** is an AI-powered personal wellness companion designed to help users track their emotional health through digital journaling and interactive AI conversations. By combining sentiment analysis with generative AI, EchoSense provides users with deep insights into their mood patterns and offers supportive, personalized feedback.

---

## 🚀 Features

-   **Intelligent Journaling**: Write or speak your thoughts. The app uses **VADER Sentiment Analysis** to understand your emotional state in real-time.
-   **Voice-to-Text Integration**: Seamlessly record diary entries using the Web Speech API for a hands-free experience.
-   **Interactive AI Companion**: Chat with a specialized AI (powered by **Google Gemini**) that provides empathetic responses and wellness tips based on your current mood.
-   **Visual Mood Board**: Track your emotional journey over time with dynamic charts (Chart.js) showing weekly and monthly mood trends.
-   **Secure Authentication**: JWT-based secure login and signup system to protect your personal reflections.

---

## 🛠️ Tech Stack

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: MongoDB (with Motor for async integration)
-   **AI/ML**: Google Gemini AI (Generative AI), VADER Sentiment Analysis
-   **Security**: JWT (JSON Web Tokens), Bcrypt for password hashing

### Frontend
-   **Core**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
-   **Visualization**: Chart.js
-   **Icons**: Font Awesome

---

## ⚙️ Local Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/JuhiGoyal/EchoSense.git
    cd EchoSense
    ```

2.  **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Create a `.env` file based on `.env.example`:
    ```env
    DATABASE_URL=your_mongodb_uri
    GEMINI_API_KEY=your_google_ai_api_key
    SECRET_KEY=your_secret_key
    ```

5.  **Run the App**:
    ```bash
    # Start Backend
    uvicorn main:app --reload --port 8001
    
    # Start Frontend (in a separate terminal)
    cd frontend
    python -m http.server 5500
    ```

---

## ⚠️ Important Note for Reviewers

> [!NOTE]
> This project utilizes several third-party APIs (Google Gemini, MongoDB Atlas) and free-tier hosting services. 
> 
> Due to **shared API quotas** across multiple development deployments and **token exhaustion limits** on free AI tiers, some features (like AI chat responses or sentiment analysis) may occasionally experience delays or fail if the monthly quota has been reached. This is a limitation of the free-tier API usage and does not reflect the core application logic.

---

## 👩‍💻 Author
**Juhi Goyal**
-   LinkedIn: [linkedin.com/in/-juhi-goyal](http://www.linkedin.com/in/-juhi-goyal)
-   Email: [juhigoyal1001@gmail.com](mailto:juhigoyal1001@gmail.com)
-   Portfolio: [JuhiGoyal/EchoSense](https://github.com/JuhiGoyal/EchoSense)
