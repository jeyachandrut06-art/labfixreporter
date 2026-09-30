# LabFix - Complete Flask + Supabase Project

## 1. Project structure

```text
LabFix_Project/
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── supabase_schema.sql
├── templates/
│   ├── index.html
│   └── submitted.html
└── static/
    ├── style.css
    ├── app.js
    └── submitted.css
```

## 2. Create the database

Open Supabase -> SQL Editor.

Paste the complete contents of `supabase_schema.sql` and click Run.

It creates:

- reports.id
- reports.student_name
- reports.lab_name
- reports.pc_number
- reports.problem_type
- reports.description
- reports.status
- reports.created_at

## 3. Create Python environment

Open this folder in VS Code.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Create .env

Copy `.env.example` to a new file named `.env`.

Put your real Supabase values there:

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
```

The service-role key is a secret. Never paste it into HTML, JavaScript, GitHub, or a public website.

## 5. Start the server

```powershell
python app.py
```

Then open:

http://127.0.0.1:5000

## 6. Test database connection

Open:

http://127.0.0.1:5000/api/health

A working setup returns JSON similar to:

```json
{
  "status": "ok",
  "database": "connected"
}
```

## 7. Submission flow

1. User fills the form.
2. `static/app.js` sends JSON to `POST /api/reports`.
3. `app.py` validates the data.
4. Flask inserts the report into Supabase.
5. Supabase returns the new report ID.
6. Flask returns a redirect URL such as `/submitted/12`.
7. JavaScript changes the browser to that URL.
8. Flask retrieves report #12 from Supabase.
9. `submitted.html` displays the submitted details.

So the confirmation page is showing data read back from the database, not just copied from the browser form.
