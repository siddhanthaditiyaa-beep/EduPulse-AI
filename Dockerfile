# Dockerfile for the EduPulse AI backend.
# Build context must be the project ROOT (the folder containing this file),
# because the backend's own code imports itself as `backend.app...`.
FROM python:3.12-slim

WORKDIR /app

# Install backend dependencies first (better layer caching)
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the backend code and the ml/ folder (the backend loads the trained
# model from ../ml/models/ relative to itself)
COPY backend/ backend/
COPY ml/ ml/

# SQLite file lives here by default — mount a persistent volume at this
# path in production so student data survives restarts/redeploys.
ENV DATABASE_URL=sqlite:////app/data/personalized_learning.db
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
