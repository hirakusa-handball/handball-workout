# Apps Script Setup (No Google Cloud)

## 1) Prepare one spreadsheet

- Create one spreadsheet file.
- Create two sheets:
  - `workout_menu`
  - `daily_menu`

## 2) Add backend script

1. Open the spreadsheet.
2. Click `Extensions` -> `Apps Script`.
3. Replace default code with `scripts/apps_script_backend.gs`.
4. Save project.

## 3) Configure API key in script properties

1. In Apps Script, open `Project Settings`.
2. Find `Script Properties`.
3. Add key: `APP_API_KEY`
4. Add value: any long random secret string.

## 4) Deploy web app

1. Click `Deploy` -> `New deployment`.
2. Type: `Web app`.
3. Execute as: `Me`.
4. Who has access: `Anyone`.
5. Deploy and copy `Web app URL`.

## 5) Configure Streamlit secrets

Create `.streamlit/secrets.toml` from `.streamlit/secrets.toml.example` and set:

```toml
[apps_script]
web_app_url = "PASTE_WEB_APP_URL"
api_key = "PASTE_THE_SAME_APP_API_KEY"
```

## 6) Seed default data (optional)

PowerShell example:

```powershell
$env:APPS_SCRIPT_WEB_APP_URL="PASTE_WEB_APP_URL"
$env:APPS_SCRIPT_API_KEY="PASTE_THE_SAME_APP_API_KEY"
python scripts/bootstrap_sheet_data.py
```
