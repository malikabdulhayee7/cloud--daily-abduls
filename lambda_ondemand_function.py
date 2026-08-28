"""
Daily Cloud Haiku Agent - On-demand AWS-theme extension (Lambda function)
Triggered synchronously via API Gateway (POST /generate-haiku):
  1. Picks today's AWS service from a fixed rotation (by day of year)
  2. Generates an AWS-service-themed haiku with Bedrock (DeepSeek v3.2)
  3. Returns the haiku as JSON - not persisted to storage (ephemeral by design)
"""

import json
import datetime
import boto3

REGION = "us-east-1"
HAIKU_MODEL_ID = "deepseek.v3.2"

AWS_SERVICES = [
    "Amazon S3", "AWS Lambda", "Amazon EC2", "Amazon DynamoDB",
    "Amazon VPC", "AWS IAM", "Amazon CloudFront", "Amazon EventBridge",
    "Amazon Bedrock", "Amazon API Gateway", "Amazon RDS",
    "Amazon SQS", "Amazon SNS", "AWS CloudFormation",
]

bedrock = boto3.client("bedrock-runtime", region_name=REGION)


def get_todays_service():
    day_of_year = datetime.date.today().timetuple().tm_yday
    return AWS_SERVICES[day_of_year % len(AWS_SERVICES)]


def generate_haiku(service):
    prompt = (
        f"Write ONE original haiku (5-7-5 syllables, 3 lines only, no title, "
        f"no explanation, no preamble) about {service} in cloud computing. "
        f"Return ONLY the haiku text, nothing else."
    )
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
    text = result.get("choices", [{}])[0].get("message", {}).get("content")
    if text is None:
        text = result.get("content", "")
    return text.strip()


def lambda_handler(event, context):
    service = get_todays_service()

    try:
        haiku = generate_haiku(service)
    except Exception as e:
        print(f"ERROR generating haiku: {e}")
        raise

    print(f"SUCCESS: generated AWS-theme haiku about {service}")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"haiku": haiku, "service_name": service}),
    }
