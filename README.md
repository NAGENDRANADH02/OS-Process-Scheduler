# OS Process Scheduler Visualizer

A local full-stack teaching tool for visualizing CPU scheduling. The Django REST API calculates schedules and stores saved runs; the Vite/React interface animates a Gantt chart, shows metrics, compares algorithms, and replays history.

## Stack

- Backend: Django + Django REST Framework + `django-cors-headers`
- Database: MySQL in production/local MySQL mode (SQLite is the zero-setup development fallback)
- Frontend: React, Vite, Bootstrap, Framer Motion, and Recharts

## Run it

### Backend

Use Python 3.11+ and MySQL client build prerequisites if using MySQL:

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
set DB_ENGINE=mysql
set DB_NAME=scheduler
set DB_USER=root
set DB_PASSWORD=your_password
python manage.py migrate
python manage.py test scheduling
python manage.py runserver
```

Omit `DB_ENGINE` and related variables to use SQLite for immediate local development. Create the MySQL database (`CREATE DATABASE scheduler CHARACTER SET utf8mb4;`) before migrating.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI targets `http://127.0.0.1:8000/api` by default. Set `VITE_API_URL` in `frontend/.env` if necessary.

## API

`POST /api/schedule/` calculates a run. `POST /api/schedule/save/` calculates and persists it. `GET /api/schedule/history/` lists up to 100 newest saved runs.

```json
{"algorithm":"round_robin","time_quantum":2,"processes":[{"pid":"P1","arrival_time":0,"burst_time":5,"priority":2}]}
```

Algorithms: FCFS executes arrival order; SJF selects the shortest burst/remaining burst; Round Robin rotates ready processes by a time quantum; Priority selects the lowest numeric priority (preemptive variants reconsider on each clock tick). Both SJF and Priority offer preemptive and non-preemptive API modes. The comparison view uses FCFS, non-preemptive SJF, Round Robin, and non-preemptive Priority—the four top-level families—on the same workload.

## Tests

`scheduling/tests.py` contains two known cases for FCFS, SJF, Round Robin, and Priority, including the preemptive variants. Run them with `python manage.py test scheduling`.
