# EduPulse AI — Personalized Learning & Student Performance Prediction

An AI-based system that analyzes a student's academic performance and learning
patterns to predict outcomes, identify weak areas, and generate personalized
learning recommendations and study plans.

- **Frontend:** React 19 + Vite + Tailwind CSS
- **Backend:** FastAPI (Python) + SQLAlchemy + SQLite (zero-config) or MySQL
- **ML:** scikit-learn / XGBoost model for performance prediction
- **AI Tutor:** Groq LLM API (optional — the app runs fine without a key, the
  tutor just won't generate live answers)

---

## 1. Requirements

- Python 3.10+ 
- Node.js 18+ and npm
- (Optional) A free [Groq API key](https://console.groq.com) for the AI Tutor

---

## 2. Run the backend

Open a terminal in the project's **root** folder (`aiperspnalized`, the one
containing both `backend/` and `frontend/` — this matters because the
backend's own code imports itself as `backend.app...`, so Python needs to
be run from one level above it):

```bash
cd aiperspnalized
python -m venv venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

Install dependencies and start the server:

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

The backend is now running at **http://127.0.0.1:8000** (docs at
`/docs`). It uses SQLite by default and creates + seeds
`personalized_learning.db` automatically on first run — nothing else to
configure.

**Optional — enable the AI Tutor:** create a file named `.env` inside
`backend/` with:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 3. Run the frontend

Open a **second terminal** in the project's **`frontend`** folder:

```bash
cd aiperspnalized/frontend
npm install
npm run dev
```

The app opens at **http://localhost:5173**. It automatically proxies
`/api` calls to the backend at `http://127.0.0.1:8000`, so keep both
terminals running at the same time.

---

## 4. Building for production / hosting

```bash
cd aiperspnalized/frontend
npm run build
```

This outputs a static site to `frontend/dist/`, which can be deployed to
any static host (Vercel, Netlify, GitHub Pages). The backend can be
deployed separately (Render, Railway, a VM) — just point the frontend's
`/api` requests at your deployed backend URL instead of the local proxy
when you deploy.

---

## 5. Deploying it live (free)

Deploy the frontend and backend to two separate free hosts:

**Backend → Fly.io** (needs a card for identity verification, but the free
allowance — 3 small VMs + 1GB volume — costs nothing for a project like this):

```bash
cd aiperspnalized
curl -L https://fly.io/install.sh | sh      # macOS/Linux
# Windows PowerShell instead: iwr https://fly.io/install.ps1 -useb | iex

fly auth signup                              # or: fly auth login
fly launch --no-deploy                       # detects the Dockerfile; say NO to adding a Postgres/Redis database
fly volumes create data --size 1             # 1GB persistent disk for the SQLite file
```

Open the `fly.toml` file it created and add this so the volume is mounted
where the app expects its database:

```toml
[mounts]
  source = "data"
  destination = "/app/data"
```

Then set your secrets and deploy:

```bash
fly secrets set JWT_SECRET_KEY=some-long-random-string GROQ_API_KEY=your_groq_key
fly deploy
fly open   # opens https://your-app-name.fly.dev — check /docs loads
```

**Frontend → Vercel** (genuinely free, no card needed):

1. Push this project to GitHub (see section 6 below) if you haven't already.
2. Go to vercel.com → **Add New Project** → import your GitHub repo.
3. Set **Root Directory** to `frontend`.
4. Framework preset: **Vite** (auto-detected).
5. Under **Environment Variables**, add:
   `VITE_API_BASE_URL` = `https://your-app-name.fly.dev/api`
6. Click **Deploy**. You'll get a live URL like `your-project.vercel.app`.

That's it — the frontend on Vercel talks to the backend on Fly.io over the
internet, the same way it talks to your local backend during development.

## 6. Project structure

```
aiperspnalized/
├── frontend/     React app (UI, all pages, components)
├── backend/      FastAPI app (auth, routes, services, ML integration)
└── ml/           Training data, trained model, training/evaluation scripts
```

---

## 7. Design

The UI is built for two groups new to using AI tools — school-age learners
and older adults — so it favors large text, high-contrast warm colors,
icon+label navigation, and plain language over dense dashboards. See
`frontend/src/index.css` and `frontend/src/components/ui/Kit.jsx` for the
design system (colors, type, shared components).
