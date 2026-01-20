# 🎬 Movie Recommendation RAG Chatbot

A beginner‑friendly **Movie Recommendation Chatbot** built using **Flask + Streamlit + RAG (Retrieval Augmented Generation)**.

The system:

* Recommends movies from a dataset using **vector similarity search**
* Remembers user preferences ("I like sci‑fi movies")
* Uses **JWT authentication** (Register → Login → Chat)
* Optionally uses **Gemini LLM** to explain recommendations

---

## 🧠 High‑Level Architecture

```
User (Streamlit UI)
        │
        ▼
Flask Backend (JWT Auth)
        │
        ├── User DB (users, preferences)
        ├── Vector DB (movie embeddings)
        └── Gemini (explanation – optional)
```

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* JWT (PyJWT)
* bcrypt (password hashing)
* Gemini
* Sentence Transformers
* Pandas / NumPy

### Frontend

* Streamlit

### Data

* Kaggle **Movies Metadata Dataset**
* Vector embeddings for semantic search

---

## 📂 Project Structure

```
Movie-Recommendation/
│
├── backend/
│   ├── app.py            # Flask API
│   ├── auth.py           # JWT logic
│   ├── db.py             # DB helpers
│   ├── rag_engine.py     # RAG + vector search
│   ├── movies_metadata.csv
│   └── .env
│
├── frontend/
│   └── streamlit_app.py  # Streamlit UI
│
└── README.md
```

---

## 🔐 Authentication Flow (Simple)

1. User **registers** (username + password)
2. Password is **hashed** and stored
3. User **logs in**
4. Backend returns a **JWT token**
5. Streamlit stores token in session
6. Token is sent with every `/chat` request

---

## 🧠 RAG Flow (Very Simple)

Example:

> "I like sci‑fi movies"

1. Sentence is converted into an **embedding (vector)**
2. Compared with movie vectors in dataset
3. Top similar movies are retrieved
4. Optional: OpenAI explains *why* they were recommended

---

## 🧪 API Endpoints

### ✅ Register

```
POST /register
```

```json
{
  "username": "pratik",
  "password": "password123"
}
```

---

### ✅ Login

```
POST /login
```

```json
{
  "username": "pratik",
  "password": "password123"
}
```

Response:

```json
{
  "token": "JWT_TOKEN"
}
```

---

### ✅ Chat

```
POST /chat
Authorization: Bearer <JWT_TOKEN>
```

```json
{
  "message": "Recommend sci‑fi movies"
}
```

Response:

```json
{
  "movies": ["Interstellar", "The Matrix"],
  "explanation": "These movies match your interest in science fiction...",
  "memory": ["I like sci‑fi movies"]
}
```

---

## 🧠 User Memory (Preferences)

If user types:

> "I like horror movies"

The system:

* Detects preference
* Stores it in DB
* Uses it for future recommendations

---

## ▶️ How to Run

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Set Environment Variables (`.env`)

```env
GEMINI_API_KEY=your_key_here
JWT_SECRET=super-secret-key
TOKEN_EXPIRE_MINUTES=60
```

---

### 4️⃣ Run Backend

```bash
cd backend
python app.py
```

---

### 5️⃣ Run Frontend

```bash
cd frontend
streamlit run streamlit_app.py
```

---

## ✅ Features Implemented

* ✅ JWT Authentication
* ✅ Password hashing
* ✅ RAG movie search
* ✅ Vector similarity search
* ✅ Long‑term user memory
* ✅ Streamlit UI
* ✅ Gemini integration (optional)
* ✅ Graceful error handling

---



