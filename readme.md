# KUL FLIGHT ETL & DASHBOARD
**Real-Time Data Engineering Pipeline / 運行情報**

This project is an automated ETL pipeline that extracts live flight data from Kuala Lumpur International Airport (KUL) and displays it on a Japanese-terminal style dashboard.

## Architecture
- **Extract**: Python (Requests) fetching from Aviationstack API.
- **Transform**: Pandas for data cleaning and type conversion.
- **Load**: SQLite database (`flight.db`) for historical storage.
- **Automation**: GitHub Actions running on a schedule (08:00 MYT).
- **Presentation**: Streamlit Dashboard with a "Nagoya Terminal" aesthetic.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your `API_KEY` to a `.env` file or GitHub Secrets.
4. Run the dashboard: `streamlit run dashboard.py`.

## Automation
This pipeline is fully automated. It wakes up at 08:00 AM MYT daily, fetches the latest flight schedules, and updates the database without manual intervention.


## API Configuration

To run this pipeline, you will need an API key from Aviationstack.

1. **Sign up here**: [Get your Aviationstack API Key](https://apilayer.com?fpr=kelocker)
2. Create a `.env` file in the root directory.
3. Add your key: `API_KEY=your_key_here`