# AEGIS

**AEGIS** is a high-performance web-based surveillance system designed to aggregate, manage, and monitor IP camera feeds. Inspired by the security protocols of the Aperture Science facility, this project bridges the gap between low-level media streaming and modern web interfaces.

> *"I'm not a human. I'm a system. A system designed to protect this facility."* — **AEGIS**

-----

## 🚀 Key Features

  * **Multi-Stream Dashboard:** Monitor multiple RTSP/HTTP streams simultaneously with low latency.
  * **Asynchronous Engine:** Powered by FastAPI for non-blocking I/O, essential for high-concurrency video handling.
  * **Dynamic Configuration:** Add, edit, or group cameras via a clean, reactive UI.
  * **Aperture UI/UX:** A sleek, industrial interface built with Vue 3 and inspired by 1970s brutalist tech aesthetics.
  * **Security Logs:** Real-time logging of camera statuses and system events.

-----

## 🛠 Tech Stack

### Backend

  * **Python 3.10+** (The core language).
  * **FastAPI:** High-performance asynchronous framework.
  * **SQLAlchemy / SQLModel:** Modern ORM for managing the camera database.
  * **OpenCV & FFmpeg:** For frame capturing and stream transcoding.
  * **Uvicorn:** Lightning-fast ASGI server implementation.

### Frontend

  * **Vue 3 (Composition API):** For a scalable and reactive frontend.
  * **Vite:** The fastest build tool for the modern web.
  * **Pinia:** Intuitive state management for camera feeds and user sessions.
  * **Tailwind CSS:** For rapid, utility-first UI development.

-----

## 📂 Project Structure

```text
aegis-system/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/            # API Endpoints (v1)
│   │   ├── core/           # Security & Config
│   │   ├── models/         # Database Schemas
│   │   ├── services/       # Video Processing Logic
│   │   └── main.py         # Entry point
│   ├── migrations/         # Alembic DB Migrations
│   └── requirements.txt
├── frontend/               # Vue.js Application
│   ├── src/
│   │   ├── components/     # UI Kit & Player Components
│   │   ├── stores/         # Pinia Global State
│   │   └── views/          # Pages (Dashboard, Settings)
│   └── package.json
└── docker-compose.yml       # Production-ready orchestration
```

-----

## 🚦 Quick Start

### 1\. Initialize the Facility (Backend)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2\. Activate the Terminal (Frontend)

```bash
cd frontend
npm install
npm run dev
```

-----


## 📈 Roadmap

  - [ ] **WebRTC Integration:** Move from MJPEG/HLS to WebRTC for sub-second latency.
  - [ ] **Motion Detection:** Integrated OpenCV analysis to trigger "Intruder" alerts.
  - [ ] **Telegram Bot:** Real-time snapshots sent to your mobile device upon motion.
  - [ ] **Archiving:** Securely store footage on local or S3 storage.

-----

## 🛡 Disclaimer

*This project is a fan-made tribute to the Portal universe and is intended for educational and portfolio purposes only. Aperture Science, AEGIS, and Portal are trademarks of Valve Corporation.*

-----

### Would you like me to generate the `app/main.py` file now, including the custom AEGIS startup message in the terminal?