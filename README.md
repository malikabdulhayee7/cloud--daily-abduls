# 🌩️ Daily Cloud Haiku: An Autonomous Creative Agent

[![AWS Builder Center](https://img.shields.io/badge/AWS-Builder_Center_Challenge-FF9900?logo=amazonaws)](https://builder.aws.com/)
[![AWS Services](https://img.shields.io/badge/Services-EventBridge%20%7C%20Lambda%20%7C%20Bedrock%20%7C%20S3-232F3E?logo=amazon)](https://aws.amazon.com/)
[![Language](https://img.shields.io/badge/Language-Python_3.12-3776AB?logo=python)](https://www.python.org/)

**Live Gallery:** [View the Latest Haikus Here](http://cloud--daily-abduls.s3-website-us-east-1.amazonaws.com)

## 📖 Overview
**Daily Cloud Haiku** is an always-on, autonomous agent built for the **AWS Builder Center Weekend Challenge: Set Your Creative App Free**.

As a DevSecOps engineer, my world is filled with repetitive logs and alerts. This agent turns that world into something reflective. Every day, without any human intervention, it generates an original 5-7-5 haiku about a random cloud/DevOps concept, styled subtly by the real-time weather in Lahore, Pakistan.

The best tool is the one you never have to open — this agent wakes up, creates, publishes, and goes back to sleep on its own.

## 🏗️ Architecture & Autonomous Flow

This application is 100% serverless and event-driven. There is no manual trigger.

```text
 🕒 EventBridge Scheduler (Daily Cron @ 3 AM PKT)
        │
        ▼
 ⚙️ AWS Lambda (Python 3.12 Orchestrator)
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
```

## ⚙️ Core Workflow (No Human in the Loop)
1. **Trigger:** An **Amazon EventBridge Scheduler** rule fires daily based on a cron expression.
2. **Context Gathering:** The **Lambda function** invokes a free weather API (`wttr.in`) to get current conditions, and randomly selects a DevOps topic (e.g., CI/CD, IAM, failovers).
3. **Creative Generation:** The context is passed as a prompt to **Amazon Bedrock** (using the `deepseek.v3.2` model) to craft a unique haiku.
4. **Publishing:** The output is saved to an **S3 bucket** configured for Static Website Hosting. It updates a rolling `latest.json` file so the frontend automatically displays the newest creation.

## 🛠️ AWS Services Used
*   **Amazon EventBridge Scheduler:** Handles the autonomous daily cron trigger.
*   **AWS Lambda:** The core computing engine that orchestrates APIs and Bedrock calls.
*   **Amazon Bedrock:** Provides the LLM (DeepSeek V3.2) for the creative text output.
*   **Amazon S3:** Stores the generated JSON artifacts and hosts the static HTML gallery.
*   **AWS IAM:** Enforces least-privilege execution roles for Lambda (Bedrock invoke, S3 write, CloudWatch logs).
*   **Amazon CloudWatch:** Captures execution logs to verify autonomous, scheduled runs.

## 📂 Repository Structure
*   `lambda_function.py`: The serverless backend logic (Context -> LLM -> Storage).
*   `index.html`: The lightweight, S3-hosted frontend that reads from `latest.json`.
*   `README.md`: Project documentation and architecture details.

## 👨‍⚖️ Note for Evaluators: Proof of Autonomy
To satisfy the challenge requirement of *"producing creative output without manual user initiation,"* this agent runs entirely via an **EventBridge Scheduler** cron rule, which invokes the Lambda function directly with no human interaction. The live gallery updates automatically every day as new scheduled runs complete — each dated entry in `data/YYYY-MM-DD.json` corresponds to a scheduled execution rather than a manual trigger.

## Setup Notes
If you want to deploy your own copy:
1. Create an S3 bucket, enable static website hosting, and set a bucket policy allowing public `GetObject` on `index.html`, `gallery/*`, and `data/*`
2. Create an IAM role for Lambda with Bedrock invoke + S3 read/write + CloudWatch logging permissions
3. Deploy `lambda_function.py` as a Lambda function (Python 3.12, 256MB memory, 30s timeout), update `BUCKET_NAME` and `HAIKU_MODEL_ID` at the top of the file to match your setup
4. Upload `index.html` to the bucket root
5. Create an EventBridge Scheduler rule with a daily cron expression targeting the Lambda function

Built as part of the AWS Builder Center Weekend Challenge, August 2026.
