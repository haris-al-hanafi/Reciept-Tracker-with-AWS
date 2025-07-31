# 🧾 Receipt Tracking System | AWS-Powered Automation 💡

A serverless, intelligent receipt tracking solution built on **AWS**. It automatically extracts key information from uploaded receipts, stores structured data in **DynamoDB**, and notifies users via **SES email** — all triggered seamlessly by an **S3 upload**.

---

## 🔧 What It Does

* 📥 Upload a receipt to **S3**
* 🧠 Extract data using **Textract**
* 📦 Save structured data to **DynamoDB**
* 📨 Send a styled summary email via **SES**

---

## 🚀 How to Start?

Follow these steps to set up and deploy your **Receipt Tracking System**:

---

### 🪣 1. Create an S3 Bucket

* Go to the **AWS S3 Console**.
* Create a new bucket (e.g., `aws-bucket-reciept-sorter`).
* Inside the bucket, create a folder (e.g., `receipts/`) to store uploaded receipt files.

---

### 📊 2. Create a DynamoDB Table

* Go to the **AWS DynamoDB Console**.
* Create a new table with the following configuration:

  * **Partition Key**: `receipt_id` (String)
  * **Sort Key**: `date` (String)

---

### 📧 3. Set Up SES (Simple Email Service)

* Go to the **Amazon SES Console**.
* Verify your **sender email address** (e.g., `your-email@example.com`).
* If you're in the **SES sandbox**, verify the **recipient email** as well.

---

### 🔐 4. Create an IAM Role for Lambda

* Go to the **IAM Console** and create a new role for Lambda.
* Attach these managed policies:

  * `AmazonDynamoDBFullAccess`
  * `AmazonS3ReadOnlyAccess`
  * `AmazonTextractFullAccess`
  * `AmazonSESFullAccess`
  * `AWSLambdaBasicExecutionRole`

---

### 🧠 5. Create a Lambda Function

* Go to the **AWS Lambda Console**.
* Create a new function (e.g., `receiptProcessor`) using Python.
* Assign the IAM role created earlier.
* Paste your Python code into the Lambda function.

---

### ⚙️ 6. Configure Environment Variables

In the **Lambda > Configuration > Environment Variables** section, add:

| Variable              | Description                       |
| --------------------- | --------------------------------- |
| `DYNAMODB_TABLE`      | Name of your DynamoDB table       |
| `SES_SENDER_EMAIL`    | Verified SES sender email         |
| `SES_RECIPIENT_EMAIL` | Recipient email for notifications |

---

### ⏱️ 7. Set Lambda Timeout

* Go to **Lambda > Configuration > General configuration**.
* Set the timeout to **3–4 minutes** to handle large receipt processing.

---

### 🔀 8. Configure S3 Event Trigger

* Go to your **S3 Bucket > Properties > Event notifications**.
* Create a new event notification:

  * Event type: **Object Created (All)**
  * Destination: **Lambda Function**
  * Choose your Lambda function (e.g., `receiptProcessor`)

---

### ✅ 9. You're All Set!

Upload a receipt (JPG, PNG, or PDF) into the `receipts/` folder. The workflow will:

1. Extract data using Textract
2. Save it in DynamoDB
3. Email you a summary via SES

---

## 📊 Architecture Overview

```plaintext
[S3 Bucket: aws-bucket-reciept-sorter]
        │
     (Upload)
        ▼
[Lambda Function - Python]
        │
 ┌───────┬────────┬────────┬────────┐
 ▼      ▼            ▼            ▼
Textract   DynamoDB     SES     CloudWatch Logs
(Extract)   (Store)   (Notify)     (Monitor)
```

---

## 📂 Folder Structure

```plaintext
aws-bucket-reciept-sorter/
└── receipts/
    ├── 2024-07-01-receipt.jpg
    ├── grocery_2024_07_10.png
    └── ...
```

---

## 🚀 Services Used

| Service             | Role                                           |
| ------------------- | ---------------------------------------------- |
| **Amazon S3**       | Stores uploaded receipts                       |
| **Amazon Textract** | Extracts vendor, date, total amount, and items |
| **Amazon DynamoDB** | Stores structured receipt data                 |
| **Amazon SES**      | Sends formatted email notifications            |
| **AWS Lambda**      | Orchestrates the entire pipeline               |
| **IAM Roles**       | Grants permission to services securely         |

---

## 🔒 Required IAM Policies

The Lambda role must include these policies:

* AmazonDynamoDBFullAccess
* AmazonS3ReadOnlyAccess
* AmazonTextractFullAccess
* AmazonSESFullAccess
* AWSLambdaBasicExecutionRole

---

## 📃 DynamoDB Schema

| Attribute      | Type   | Description                 |
| -------------- | ------ | --------------------------- |
| `receipt_id`   | String | Unique ID (Partition Key)   |
| `date`         | String | Date of receipt (Sort Key)  |
| `vendor`       | String | Vendor/merchant name        |
| `total`        | String | Total amount spent          |
| `items`        | List   | Extracted line items        |
| `s3_path`      | String | Full S3 path of the receipt |
| `processed_at` | String | ISO timestamp of processing |

---

## ⚙️ Lambda Environment Variables

| Variable              | Description                            |
| --------------------- | -------------------------------------- |
| `DYNAMODB_TABLE`      | Name of the DynamoDB table             |
| `SES_SENDER_EMAIL`    | Verified SES email address (sender)    |
| `SES_RECIPIENT_EMAIL` | Email address to receive notifications |

---

## 🚀 How It Works (Behind the Scenes)

**Upload Trigger**
User uploads a .jpg, .png, or .pdf file to the `receipts/` folder in S3.

**Lambda Executes**
The event triggers a Python Lambda function.

**Textract Analyzes**
Textract's `AnalyzeExpense` API extracts structured data from the receipt.

**Data Stored**
Parsed data is stored in DynamoDB with metadata.

**Email Notification**
A styled SES email summarizes the extracted information.

---

### 📢 Sample Email Output

**Subject**: Receipt Processed - Amazon - \$42.55

```
Hello,

Your receipt has been processed.

Vendor: Amazon
Date: 2024-07-01
Total: $42.55
Items:
- USB Cable - $12.00 x 2
- Power Bank - $18.55 x 1

Stored at: s3://aws-bucket-reciept-sorter/receipts/amazon_receipt.jpg
```

---

> Built with ❤️ and AWS ✨
