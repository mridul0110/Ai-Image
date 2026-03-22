# VintageLogin ■

> Full-Stack Flask App · PostgreSQL on Neon · AI Vision · Render Hosting

**Built by Mridul** 

---

## 🌐 Live Demo



Register an account, pick your pixel buddy, and drop an image for an AI-powered analysis.
> ⏳ *First load may take ~30 seconds on the free tier as the server wakes up.*

---

## 📖 Overview

VintageLogin is a full-stack web application featuring:

- 🔐 Secure user registration & login (passwords hashed with Werkzeug)
- 🐘 Cloud PostgreSQL database via **Neon**
- 🤖 AI image analysis using **NVIDIA NIM (Phi-3.5 Vision)**
- 🐾 7 pixel animal companions, each with a unique personality
- 🎨 Vintage parchment UI — Cormorant Garamond + Jost fonts
- 🖼️ Drag & drop image upload with typing-animation responses
- 🐳 Dockerised and deployed on **Render**

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python 3.10 + Flask | Web framework & routing |
| ORM | Flask-SQLAlchemy | Database models & queries |
| Auth | Flask-Login + Werkzeug | Session management & password hashing |
| Database | PostgreSQL via Neon | Cloud database |
| AI Vision | NVIDIA NIM Phi-3.5 Vision | Personality-driven image analysis |
| Frontend | HTML + CSS + Vanilla JS | Vintage UI, animations, drag & drop |
| Fonts | Cormorant Garamond + Jost | Vintage serif + geometric sans |
| Server | Gunicorn | Production WSGI server |
| Deployment | Docker + Render | Container deployment on port 10000 |

---

## 📁 File Structure

```
ImageAnalyzer/
├── app.py               # Flask app factory, session config, blueprints
├── auth.py              # Login, register, logout routes
├── main.py              # Dashboard route + /describe API endpoint
├── models.py            # SQLAlchemy User model
├── vision.py            # NVIDIA NIM integration + 7 buddy personalities
├── config.py            # App config, PostgreSQL SSL + pool settings
├── Dockerfile           # Render Docker deployment (port 10000)
├── requirements.txt     # Python dependencies
├── .gitignore           # Excludes .env, instance/, migrations/
├── .env.example         # Template for local development
│
├── static/
│   ├── css/style.css    # Vintage parchment UI — all styles
│   └── js/script.js     # Buddy animations, typing effect, image upload
│
└── templates/
    ├── login.html        # Login page
    ├── register.html     # Registration page
    └── dashboard.html    # Main dashboard — buddy panel + image drop zone
```

---

## 🔄 Application Workflow

### Authentication
1. **Register** → name, email, password submitted → password hashed → saved to Neon DB → session created
2. **Login** → credentials checked → Flask-Login session cookie signed with `SECRET_KEY`
3. **Protected routes** → cookie verified on every request → user loaded from DB
4. **Logout** → session cleared → cookie invalidated

### AI Image Analysis
1. User drags/selects image → JS reads it as base64
2. User selects a buddy (or one is randomly assigned)
3. Browser POSTs `{ image, buddy }` to `/describe`
4. Flask calls NVIDIA NIM Phi-3.5 Vision with buddy system prompt + image
5. Response typed out character-by-character in the UI

---

## 🐾 The 7 Pixel Buddies

| Buddy | Name | Personality |
|-------|------|-------------|
| 🦆 | Pip the Duck | Chaotic, excited, duck puns, ends every sentence with !! |
| 🐱 | Mochi the Cat | Dry wit, sardonic, secretly fascinated |
| 🦊 | Rusty the Fox | Clever, witty, spots what others miss |
| 🐸 | Lily the Frog | Chill philosopher, zen + random frog thoughts |
| 🐰 | Coco the Bunny | Overenthusiastic, boundless energy, pure serotonin |
| 🐻 | Bruno the Bear | Cozy gentle giant, honey metaphors, warm |
| 🐧 | Percy the Penguin | Very proper, formal, gets flustered easily |

---

## 🗄️ Database — Neon PostgreSQL

- **Provider:** Neon (neon.tech) — free tier
- **Connection:** Direct connection only — pooling must be **OFF**
- **SSL:** `sslmode=require` enforced
- **Table:** `users` — auto-created on first startup via `db.create_all()`

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| name | String(120) | Full name |
| email | String(255) | Unique login identifier |
| password_hash | String(512) | Werkzeug hashed |
| google_id | String(255) | Reserved for OAuth |
| created_at | DateTime | Auto timestamp |

---

## 🚀 Deploying on Render

1. Create account at [render.com](https://render.com) — connect GitHub
2. **New Web Service** → select this repo → Environment: **Docker**
3. Add these secrets under **Environment Variables**:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Long random string — run `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Neon connection string with `?sslmode=require` (pooling OFF) |
| `NVIDIA_API_KEY` | From [build.nvidia.com](https://build.nvidia.com) — free tier |

4. Click **Create Web Service** — Render builds and deploys automatically.

Every `git push origin main` triggers an automatic redeploy.

> **Free tier tip:** Use [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes and prevent cold starts.

---

## 🔒 Security

- Passwords hashed with Werkzeug PBKDF2 — never stored in plain text
- Sessions signed with `SECRET_KEY` — tampering detected and rejected
- All DB connections enforce `sslmode=require`
- `.env` is gitignored — secrets never reach GitHub
- Cookies: `Secure=True`, `HttpOnly=True`, `SameSite=Lax`

---