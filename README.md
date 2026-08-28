 AUTONOMOUS DAILY FLOW (no human in the loop)
 🕒 EventBridge Scheduler (Daily Cron @ 3 AM PKT)
        │
        ▼
 ⚙️ AWS Lambda: cloud-haiku-daily (Python 3.12 Orchestrator)
        │
        ├──► 🌤️ wttr.in (Fetches live weather context)
        │
        ├──► 🧠 Amazon Bedrock (DeepSeek V3.2 generates Haiku)
        │
        ▼
 🪣 Amazon S3 (Storage & Hosting)
        │
        ├──► Saves historical data (data/YYYY-MM-DD.json)
        ├──► Updates rolling state (gallery/latest.json)
        └──► Serves static UI (index.html)


 ON-DEMAND AWS-THEME FLOW (visitor-triggered)
 🖱️ Visitor clicks "Generate AWS Service Haiku" on the gallery page
        │
        ▼
 🌐 Amazon API Gateway (HTTP API, POST /generate-haiku)
        │
        ▼
 ⚙️ AWS Lambda: cloud-haiku-ondemand (Python 3.12)
        │
        ├──► Picks today's AWS service from a fixed rotation
        │
        ├──► 🧠 Amazon Bedrock (DeepSeek V3.2 generates Haiku)
        │
        ▼
 JSON response rendered instantly on the page (no reload, not persisted)
