# aws-data-pipeline-project
aws-data-pipeline-project

# Serverless Data Processing Pipeline on AWS

An event-driven serverless data processing pipeline designed to ingest data payloads, parse metric properties automatically, and track metadata metrics within a decoupled cloud design infrastructure.

## 1. Architecture Overview

The system design leverages entirely serverless AWS resources to achieve an independent, event-driven orchestration layer that scales smoothly without administrative overhead or idling infrastructure costs.

### Process Lifecycle Flow
1. **Ingestion & Triggering:** Users upload a `.csv` file into the target Amazon S3 bucket. S3 automatically captures the context and publishes an asynchronous notification payload.
2. **Compute Execution:** AWS Lambda intercepts the notification container. The Python environment runtime downloads the target file directly to memory using the `boto3` SDK.
3. **Storage & Logging:** The code counts rows and metrics and updates a structured record entry directly into the `FileProcessingMetadata` DynamoDB NoSQL collection. Standard metrics logs populate straight to AWS CloudWatch Logs.

## 2. Security & Optimization Profiles
* **Identity & Access Management (IAM):** Explicit runtime isolation is secured via granular IAM service roles implementing the **Principle of Least Privilege**.
* **Error Resilience Integration:** Features native error-handling configurations to capture encoding anomalies (such as `UnicodeDecodeError`) safely while avoiding system failure loops.
* **Serverless Cost Efficiency:** The deployment scales dynamically and operates on zero fixed costs, billed exclusively on fractions of real execution milliseconds.

## 3. Directory Layout
* `lambda_function.py` - Production handler logic executing text analysis and metadata pushes.
* `iam-policy-example.json` - Restricted access policy definition for cloud configuration deployments.
* `test_lambda.py` - Local validation script mock runner testing ingestion workflows.
