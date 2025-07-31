# 🧾 Receipt Tracking System | AWS-Powered Automation 💡

A serverless, intelligent receipt tracking solution built on **AWS**. It automatically extracts key information from uploaded receipts, stores structured data in **DynamoDB**, and notifies users via **SES email** — all triggered seamlessly by an **S3 upload**.

---

## 🔧 What It Does

📥 Upload a receipt to `S3`  
🧠 Extract data using `Textract`  
📦 Save structured data to `DynamoDB`  
📨 Send a styled summary email via `SES`

---

## 📐 Architecture Overview

```plaintext
[S3 Bucket: aws-bucket-reciept-sorter]
        │
     (Upload)
        ▼
[Lambda Function - Python]
        │
 ┌──────┼────────────┬────────────┐
 ▼      ▼            ▼            ▼
Textract   DynamoDB     SES     CloudWatch Logs
(Extract)   (Store)   (Notify)     (Monitor)

//Folder Structure

aws-bucket-reciept-sorter/
└── receipts/
    ├── 2024-07-01-receipt.jpg
    ├── grocery_2024_07_10.png
    └── ...


//Services Used

| Service             | Role                                                         |
| ------------------- | ------------------------------------------------------------ |
| **Amazon S3**       | Stores uploaded receipts in a structured folder              |
| **Amazon Textract** | Extracts vendor, date, total amount, and items from receipts |
| **Amazon DynamoDB** | Saves structured data with `receipt_id` (PK) and `date` (SK) |
| **Amazon SES**      | Sends beautifully formatted emails to notify users           |
| **AWS Lambda**      | Orchestrates the workflow end-to-end                         |
| **IAM Roles**       | Provides scoped access to each AWS service securely          |


🔐 Required IAM Permissions
The Lambda function uses an IAM role with these managed policies:

AmazonDynamoDBFullAccess

AmazonS3ReadOnlyAccess

AmazonTextractFullAccess

AmazonSESFullAccess

AWSLambdaBasicExecutionRole



| Attribute      | Type   | Description                 |
| -------------- | ------ | --------------------------- |
| `receipt_id`   | String | Unique ID (Partition Key)   |
| `date`         | String | Date of receipt (Sort Key)  |
| `vendor`       | String | Vendor/merchant name        |
| `total`        | String | Total amount spent          |
| `items`        | List   | Extracted line items        |
| `s3_path`      | String | Full S3 path of the receipt |
| `processed_at` | String | ISO timestamp of processing |



| Variable              | Description                            |
| --------------------- | -------------------------------------- |
| `DYNAMODB_TABLE`      | Name of the DynamoDB table             |
| `SES_SENDER_EMAIL`    | Verified SES email address (sender)    |
| `SES_RECIPIENT_EMAIL` | Email address to receive notifications |



🚀 How It Works (Behind the Scenes)
Upload Trigger
A user uploads a .jpg, .png, or .pdf file to the receipts/ folder in S3.

Lambda Executes
The event triggers a Python Lambda function.

Textract Analyzes
Textract's AnalyzeExpense extracts structured data from the receipt.

Data Stored
Data is parsed and saved in DynamoDB with metadata.

Email Notification
A styled email with vendor, amount, and items is sent to the recipient via SES.

Subject: Receipt Processed - Amazon - $42.55

Hello,

Your receipt has been processed.

Vendor: Amazon
Date: 2024-07-01
Total: $42.55
Items:
- USB Cable - $12.00 x 2
- Power Bank - $18.55 x 1

Stored at: s3://aws-bucket-reciept-sorter/receipts/amazon_receipt.jpg


