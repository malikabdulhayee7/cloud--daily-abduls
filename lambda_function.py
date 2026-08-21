"""
Daily Cloud Haiku Agent - Lambda function (text-only version)
Runs on a daily EventBridge Scheduler trigger:
  1. Fetches current Lahore weather (free, no API key needed - wttr.in)
  2. Generates a cloud/DevOps-themed haiku with Bedrock (DeepSeek v3.2)
  3. Saves haiku JSON to S3
  4. Updates latest.json (used by the gallery page)
"""

import json
import datetime
import random
import urllib.request
import boto3
import botocore.exceptions

# ---- CONFIG ----
BUCKET_NAME = "cloud--daily-abduls"    # <-- your S3 bucket
REGION = "us-east-1"                   # <-- region where the model is enabled
HAIKU_MODEL_ID = "deepseek.v3.2"  # confirmed from Bedrock console Model catalog
MAX_GALLERY_ITEMS = 15

CLOUD_TOPICS = [
    "a misconfigured S3 bucket", "an autoscaling group", "a Lambda cold start",
    "a CI/CD pipeline", "an IAM policy", "a Kubernetes pod crashing",
    "a firewall rule", "a database failover", "a load balancer",
    "an expired TLS certificate", "a deployment rollback", "cloud cost alerts",
]

s3 = boto3.client("s3", region_name=REGION)
bedrock = boto3.client("bedrock-runtime", region_name=REGION)


def get_lahore_weather():
    """Free weather lookup, no API key required."""
    try:
        url = "https://wttr.in/Lahore?format=%C+%t"
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception:
        return "clear skies"  # safe fallback so the agent never blocks on weather


def generate_haiku(topic, weather):
    prompt = (
        f"Write ONE original haiku (5-7-5 syllables, 3 lines only, no title, "
        f"no explanation, no preamble) about {topic}, subtly inspired by this "
        f"weather: '{weather}'. Return ONLY the haiku text, nothing else."
    )
    # DeepSeek models on Bedrock use a standard chat-style message body.
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.9,
    }
    resp = bedrock.invoke_model(
        modelId=HAIKU_MODEL_ID,
        body=json.dumps(body),
    )
    result = json.loads(resp["body"].read())
    # NOTE: response shape can vary by model provider - if this errors, print
    # `result` once in a test run and adjust the field access below to match.
    text = result.get("choices", [{}])[0].get("message", {}).get("content")
    if text is None:
        text = result.get("content", "")
    return text.strip()


def update_gallery_index(new_entry):
    """Keep a rolling latest.json with the most recent entries for the gallery page."""
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key="gallery/latest.json")
        items = json.loads(obj["Body"].read())
    except botocore.exceptions.ClientError:
        items = []

    items.insert(0, new_entry)
    items = items[:MAX_GALLERY_ITEMS]

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="gallery/latest.json",
        Body=json.dumps(items, indent=2),
        ContentType="application/json",
    )


def lambda_handler(event, context):
    date_str = datetime.date.today().isoformat()
    topic = random.choice(CLOUD_TOPICS)
    weather = get_lahore_weather()

    try:
        haiku = generate_haiku(topic, weather)
    except Exception as e:
        print(f"ERROR generating haiku: {e}")
        raise  # let it fail loudly so CloudWatch captures it; no infinite retry

    data_key = f"data/{date_str}.json"

    entry = {
        "date": date_str,
        "topic": topic,
        "weather": weather,
        "haiku": haiku,
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=data_key,
        Body=json.dumps(entry, indent=2),
        ContentType="application/json",
    )

    update_gallery_index(entry)

    print(f"SUCCESS: generated haiku for {date_str} about {topic}")
    return {"statusCode": 200, "body": json.dumps(entry)}
