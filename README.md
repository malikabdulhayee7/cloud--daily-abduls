# Daily Cloud Haiku

An always-on AWS agent built for the **AWS Builder Center Weekend Challenge: Set Your Creative App Free**.

Every day, on its own schedule, this agent:
1. Fetches the current weather in Lahore, Pakistan
2. Picks a random cloud/DevOps topic (a CI/CD pipeline, an IAM policy, a database failover, etc.)
3. Asks a Bedrock-hosted language model to write an original haiku about that topic, subtly inspired by the weather
4. Saves the haiku to S3
5. Updates a static gallery page so the newest haikus are always visible

No manual trigger, no prompt typed by a human — it just runs, and there's something new waiting when you check in.

**Live gallery:** http://cloud--daily-abduls.s3-website-us-east-1.amazonaws.com

## Architecture

```
EventBridge Scheduler (daily cron)
        |
        v
    AWS Lambda (Python 3.12)
        |
        +--> wttr.in (free weather API)
        |
        +--> Amazon Bedrock (DeepSeek V3.2) --> haiku text
        |
        v
    Amazon S3
        |
        +--> data/YYYY-MM-DD.json   (each day's haiku, permanent record)
        +--> gallery/latest.json    (rolling list, powers the gallery page)
        +--> index.html             (static gallery, served via S3 website hosting)
```

## Files in this repo

- **`lambda_function.py`** — the Lambda function: fetches weather, calls Bedrock, writes to S3
- **`index.html`** — the static gallery page that reads `gallery/latest.json` and renders haiku cards
- **`README.md`** — this file

## AWS services used

- **Amazon EventBridge Scheduler** — daily cron trigger, no manual invocation
- **AWS Lambda** — orchestrates the whole flow
- **Amazon Bedrock** (DeepSeek V3.2) — generates the haiku
- **Amazon S3** — storage + static website hosting for the gallery
- **AWS IAM** — scoped execution role for the Lambda function
- **Amazon CloudWatch Logs** — logs every run for monitoring/verification

## Setup notes

If you want to deploy your own copy:
1. Create an S3 bucket, enable static website hosting, and set a bucket policy allowing public `GetObject` on `index.html`, `gallery/*`, and `data/*`
2. Create an IAM role for Lambda with Bedrock invoke + S3 read/write + CloudWatch logging permissions
3. Deploy `lambda_function.py` as a Lambda function (Python 3.12, 256MB memory, 30s timeout), update `BUCKET_NAME` and `HAIKU_MODEL_ID` at the top of the file to match your setup
4. Upload `index.html` to the bucket root
5. Create an EventBridge Scheduler rule with a daily cron expression targeting the Lambda function

Built as part of the [AWS Builder Center Weekend Challenge](https://builder.aws.com), August 2026.
