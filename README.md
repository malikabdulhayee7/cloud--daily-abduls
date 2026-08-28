# 🌩️ Daily Cloud Haiku: An Autonomous Creative Agent

[![AWS Builder Center](https://img.shields.io/badge/AWS-Builder_Center_Challenge-FF9900?logo=amazonaws\&logoColor=white)](https://builder.aws.com/)
[![AWS Services](https://img.shields.io/badge/AWS-EventBridge%20%7C%20Lambda%20%7C%20Bedrock%20%7C%20S3-232F3E?logo=amazonaws\&logoColor=white)](https://aws.amazon.com/)
[![Language](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Serverless-orange?logo=awslambda\&logoColor=white)](https://aws.amazon.com/serverless/)

> **An always-on, serverless AI agent that turns cloud and DevOps concepts into creative daily haikus — enriched with real-time Lahore weather and published automatically to an S3-hosted gallery.**

🔗 **Live Gallery:** [View the Latest Haikus](http://cloud--daily-abduls.s3-website-us-east-1.amazonaws.com)

---

## 📖 Overview

**Daily Cloud Haiku** is an autonomous creative application built for the **AWS Builder Center Weekend Challenge: Set Your Creative App Free**.

As a DevSecOps engineer, my world is filled with infrastructure, deployments, logs, alerts, IAM policies, containers, and cloud services. This project turns that technical world into something small, creative, and reflective.

Every day, without requiring a human to start it, the system:

1. Wakes up through **Amazon EventBridge Scheduler**.
2. Fetches the current weather in **Lahore, Pakistan**.
3. Selects a random cloud/DevOps topic.
4. Uses **Amazon Bedrock + DeepSeek V3.2** to generate an original 5-7-5 haiku.
5. Stores the generated artifact in **Amazon S3**.
6. Updates a rolling gallery that the frontend displays automatically.

There is also an **on-demand AWS Service Haiku** feature. A visitor can click a button on the gallery, which calls **API Gateway → Lambda → Bedrock** and returns a generated haiku instantly without persisting it.

> **The best tool is the one you never have to open — this agent wakes up, creates, publishes, and goes back to sleep on its own.**

---

## 🏗️ Architecture

### 🤖 Autonomous Daily Flow — No Human in the Loop

```text
 🕒 EventBridge Scheduler
    Daily schedule @ 3 AM PKT
              │
              ▼
 ⚙️ AWS Lambda — Python 3.12
    Daily Cloud Haiku Agent
              │
       ┌──────┴────────┐
       ▼               ▼
 🌤️ wttr.in       🧠 Amazon Bedrock
 Lahore weather    DeepSeek V3.2
       │               │
       └──────┬────────┘
              ▼
        🪣 Amazon S3
              │
       ┌──────┼──────────────┐
       ▼      ▼              ▼
    data/   gallery/      index.html
   daily    latest.json   Static UI
    JSON
```

### ⚡ On-Demand AWS Service Flow

```text
 🖱️ Visitor clicks
    "Generate AWS Service Haiku"
              │
              ▼
 🌐 Amazon API Gateway
    POST /generate-haiku
              │
              ▼
 ⚙️ AWS Lambda — Python 3.12
    On-demand generator
              │
              ▼
 🧠 Amazon Bedrock
    DeepSeek V3.2
              │
              ▼
 📦 JSON response
    Returned directly to browser

    Result is intentionally NOT persisted.
```

---

## ⚙️ Core Workflow

### 1. Trigger

An **Amazon EventBridge Scheduler** invokes the daily Lambda automatically according to the configured schedule.

No user interaction is required.

### 2. Context Gathering

The Lambda randomly selects a cloud/DevOps topic such as:

* Lambda cold starts
* S3 buckets
* IAM policies
* CI/CD pipelines
* Kubernetes pods
* Database failovers
* Load balancers
* TLS certificates
* Deployment rollbacks
* Cloud cost alerts

It then calls `wttr.in` to obtain the current Lahore weather.

If the weather endpoint is unavailable, the function falls back to `clear skies` so the autonomous workflow can continue.

### 3. Creative Generation

The topic and weather context are passed to **Amazon Bedrock**, using the `deepseek.v3.2` model.

The prompt requests:

* One original haiku
* Exactly three lines
* A 5-7-5 syllable structure
* No title
* No explanation or additional text

### 4. Publishing

The generated entry is stored in S3 as:

```text
data/YYYY-MM-DD.json
```

The application also maintains:

```text
gallery/latest.json
```

This file contains the latest **15 entries** used by the frontend gallery.

### 5. Presentation

`index.html` is a lightweight static frontend that loads `gallery/latest.json` and renders the generated haikus as cards.

---

## 🛠️ AWS Services Used

| Service                             | Role                                                     |
| ----------------------------------- | -------------------------------------------------------- |
| 🕒 **Amazon EventBridge Scheduler** | Automatically triggers the daily agent                   |
| ⚙️ **AWS Lambda**                   | Serverless orchestration and AI workflow execution       |
| 🧠 **Amazon Bedrock**               | Generates haikus using DeepSeek V3.2                     |
| 🪣 **Amazon S3**                    | Stores daily JSON artifacts and hosts the static gallery |
| 🌐 **Amazon API Gateway**           | Provides the on-demand `POST /generate-haiku` API        |
| 🔐 **AWS IAM**                      | Controls Lambda permissions using least privilege        |
| 📊 **Amazon CloudWatch**            | Captures Lambda execution logs and failures              |

### External Service

**wttr.in** provides the current Lahore weather without requiring an API key.

---

## ✨ Key Features

* 🤖 **Fully autonomous daily generation**
* 🌤️ **Real-time Lahore weather context**
* 🧠 **Generative AI with Amazon Bedrock**
* ☁️ **Cloud & DevOps themed creative content**
* 🪣 **Persistent daily artifacts in S3**
* 🖼️ **Rolling gallery of the latest 15 haikus**
* ⚡ **On-demand AWS-service haiku generation**
* 🌐 **Static serverless frontend**
* 📦 **JSON-based data storage**
* 📊 **CloudWatch logging**
* 🔐 **IAM-based access control**
* 🚫 **No human intervention required for the daily workflow**

---

## 📂 Repository Structure

```text
cloud--daily-abduls/
│
├── index.html
│   └── Static frontend / haiku gallery
│
├── lambda_function.py
│   └── Autonomous daily agent
│       ├── Weather context
│       ├── Topic selection
│       ├── Bedrock generation
│       └── S3 persistence
│
├── lambda-on-demand.py
│   └── API-triggered AWS service haiku generator
│
└── README.md
    └── Project documentation
```

---

## 📦 Data Model

Each daily generated entry follows this structure:

```json
{
  "date": "2026-08-28",
  "topic": "a Lambda cold start",
  "weather": "Clear +32°C",
  "haiku": "Generated haiku text..."
}
```

Daily entries are stored under:

```text
data/YYYY-MM-DD.json
```

The rolling gallery is maintained at:

```text
gallery/latest.json
```

---

## ⚡ On-Demand AWS Haiku

The project also includes a visitor-triggered creative path.

When the user clicks:

**☁️ Generate AWS Service Haiku**

the browser sends:

```http
POST /generate-haiku
```

to Amazon API Gateway.

The request flows through:

```text
Browser
   ↓
API Gateway
   ↓
Lambda
   ↓
Amazon Bedrock
   ↓
Lambda
   ↓
API Gateway
   ↓
Browser
```

The Lambda chooses an AWS service from a fixed daily rotation, generates the haiku with Bedrock, and returns JSON containing:

```json
{
  "haiku": "Generated haiku...",
  "service_name": "Amazon S3"
}
```

Unlike the autonomous daily workflow, this result is **ephemeral by design** and is not written to S3.

---

## 🔐 IAM & Security

The Lambda execution roles should follow the **principle of least privilege**.

### Scheduled Lambda

Requires access broadly equivalent to:

```text
bedrock:InvokeModel
s3:GetObject
s3:PutObject
CloudWatch Logs permissions
```

### On-Demand Lambda

Requires:

```text
bedrock:InvokeModel
CloudWatch Logs permissions
```

### EventBridge

The EventBridge Scheduler requires permission to invoke the scheduled Lambda.

> **Production recommendation:** scope IAM policies to the exact S3 bucket, object paths, Lambda resources, and Bedrock model instead of using wildcard permissions.

---

## 🚀 Setup & Deployment

Want to deploy your own version?

### Prerequisites

* AWS account
* AWS CLI configured
* Python 3.12
* Amazon Bedrock access
* DeepSeek V3.2 model access in your selected AWS Region
* S3 permissions
* Lambda permissions
* EventBridge Scheduler permissions
* API Gateway permissions for the on-demand feature

---

### 1. Create the S3 Bucket

Create an S3 bucket and configure it for static website hosting.

The application expects:

```text
index.html
gallery/latest.json
data/YYYY-MM-DD.json
```

If making the gallery publicly accessible through S3 website hosting, configure the appropriate bucket/object access policy.

---

### 2. Deploy the Daily Lambda

Create an **AWS Lambda Python 3.12** function using:

```text
lambda_function.py
```

The current implementation uses:

```python
BUCKET_NAME = "cloud--daily-abduls"
REGION = "us-east-1"
HAIKU_MODEL_ID = "deepseek.v3.2"
MAX_GALLERY_ITEMS = 15
```

For your own deployment, replace these values with your resources.

---

### 3. Configure EventBridge Scheduler

Create a daily EventBridge Scheduler schedule targeting the Lambda.

The project is designed around:

```text
3:00 AM PKT
```

Use the scheduler's timezone-aware configuration so the schedule remains aligned with Pakistan Standard Time.

---

### 4. Deploy the On-Demand Lambda

Create another Python 3.12 Lambda using:

```text
lambda-on-demand.py
```

Expose it through an **API Gateway HTTP API** route:

```text
POST /generate-haiku
```

Configure CORS for the frontend origin.

---

### 5. Configure the Frontend

In `index.html`, point the API URL to your API Gateway endpoint:

```javascript
const API_URL =
  "https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/generate-haiku";
```

Upload `index.html` to the S3 bucket root.

---

### 6. Test the System

Verify that:

* EventBridge invokes Lambda.
* Weather data is retrieved.
* Bedrock generates the haiku.
* S3 receives the daily JSON object.
* `gallery/latest.json` is updated.
* The static frontend loads the gallery.
* API Gateway successfully invokes the on-demand Lambda.
* The browser receives the generated AWS-service haiku.
* CloudWatch contains successful execution logs.

---

## 🧪 Reliability & Error Handling

The application includes simple failure handling to make the autonomous workflow more resilient.

### Weather Failure

If `wttr.in` cannot be reached, the daily Lambda uses:

```text
clear skies
```

as a fallback.

### Bedrock Failure

Bedrock errors are logged and re-raised so the Lambda invocation is marked as failed and the issue can be investigated through CloudWatch.

### Gallery State

The gallery is intentionally bounded to the latest **15 entries** instead of growing indefinitely.

---

## ⚠️ Important Implementation Note

The prompt asks DeepSeek to produce a **5-7-5 haiku**, but the current application does not perform deterministic syllable counting after generation.

Therefore, the 5-7-5 structure is currently a **model instruction rather than a formally validated constraint**.

A future version could add automatic syllable counting and regeneration until a valid 5-7-5 structure is produced.

---

## 🎯 Proof of Autonomy — For Evaluators

The core requirement of the challenge is that the application should produce creative output **without requiring manual initiation**.

This project satisfies that requirement through the following autonomous chain:

```text
EventBridge Scheduler
        ↓
AWS Lambda
        ↓
Weather + Random Topic
        ↓
Amazon Bedrock
        ↓
Generated Haiku
        ↓
Amazon S3
        ↓
Live Gallery
```

There is **no human trigger in the daily generation path**.

Each daily artifact is written to the S3 `data/` path by the scheduled Lambda execution.

The visitor-triggered API feature is separate and exists as an additional interactive experience — it does **not** replace the autonomous daily workflow.

---

## 💡 What This Demonstrates

Although the application is intentionally playful, the underlying architecture demonstrates several production-relevant cloud patterns:

* Event-driven serverless architecture
* Scheduled automation
* AI inference with a managed foundation-model service
* External API integration
* Object-based persistence
* Static web hosting
* HTTP API integration
* IAM-based access control
* CloudWatch observability
* Stateless Lambda workloads
* Separation between scheduled and user-triggered workflows

The same architecture pattern can be adapted for practical applications such as:

* 📊 Daily cloud operations summaries
* 📝 Automated infrastructure reports
* 🤖 AI-generated DevOps documentation
* 💰 Cloud cost summaries
* 📈 Engineering dashboards
* 🚨 Scheduled incident-analysis reports
* 📰 Automated knowledge digests

---

## 🔮 Future Improvements

* [ ] Add deterministic 5-7-5 syllable validation.
* [ ] Move configuration to Lambda environment variables or AWS Systems Manager Parameter Store.
* [ ] Add AWS SAM / CloudFormation / CDK infrastructure as code.
* [ ] Add GitHub Actions CI/CD.
* [ ] Add automated unit tests.
* [ ] Add CloudWatch alarms and custom metrics.
* [ ] Add API throttling/authentication for the on-demand endpoint.
* [ ] Restrict CORS to the production frontend origin.
* [ ] Put CloudFront in front of the S3 website.
* [ ] Add a custom domain with HTTPS.
* [ ] Track Bedrock latency and token usage.
* [ ] Add richer historical search and filtering.

---

## 🏆 Built for the AWS Builder Center Challenge

Built as part of the **AWS Builder Center Weekend Challenge — Set Your Creative App Free**, August 2026.

The goal was simple:

> **Take an ordinary technical workflow and let an autonomous cloud-based agent turn it into something unexpectedly creative.**

Cloud infrastructure doesn't have to be boring.

**Sometimes a Lambda wakes up and writes poetry. ☁️**

---

## 👨‍💻 Author

**Abdul Hayee**

Cloud & DevOps Engineer | AWS | Azure | GCP | Kubernetes | CI/CD

GitHub: [@malikabdulhayee7](https://github.com/malikabdulhayee7)

---

## 📄 License

No explicit open-source license is currently included in this repository.

Add a `LICENSE` file if you want to distribute the project under a specific open-source license.
