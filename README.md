# 🧾 Receipt Tracking System | AWS-Powered Automation 💡

A serverless, intelligent receipt tracking solution built on **AWS**. It automatically extracts key information from uploaded receipts, stores structured data in **DynamoDB**, and notifies users via **SES email** — all triggered seamlessly by an **S3 upload**.

---

## 🔧 What It Does

📥 Upload a receipt to `S3`  
🧠 Extract data using `Textract`  
📦 Save structured data to `DynamoDB`  
📨 Send a styled summary email via `SES`

---

Here's your **"How to Start?"** section rewritten with improved grammar, clarity, and structure. It follows a clean step-by-step format to help users understand the setup process easily.

---

## 🚀 How to Start?

Follow these steps to set up and deploy your **Receipt Tracking System**:

---

### 🪣 1. Create an S3 Bucket

* Go to the AWS S3 Console.
* Create a new bucket (e.g., `aws-bucket-reciept-sorter`).
* Inside the bucket, create a folder (e.g., `receipts/`) to store uploaded receipt files.

---

### 📊 2. Create a DynamoDB Table

* Go to the AWS DynamoDB Console.
* Create a new table with:

  * **Partition Key**: `receipt_id` (String)
  * **Sort Key**: `date` (String)

---

### 📧 3. Set Up SES (Simple Email Service)

* Navigate to the **Amazon SES Console**.
* Verify your **sender email address** (e.g., `your-email@example.com`).
* If you're in the **SES sandbox environment**, verify the recipient email as well.

---

### 🔐 4. Create an IAM Role for Lambda

* Go to the IAM Console and create a new role for Lambda.
* Attach the following policies:

  * `AmazonDynamoDBFullAccess`
  * `AmazonS3ReadOnlyAccess`
  * `AmazonTextractFullAccess`
  * `AmazonSESFullAccess`
  * `AWSLambdaBasicExecutionRole`

---

### 🧠 5. Create a Lambda Function

* Go to the **AWS Lambda Console**.
* Create a new function using Python (e.g., `receiptProcessor`).
* Assign the IAM role you just created.
* Paste the refactored Lambda code into the function.

---

### ⚙️ 6. Configure Environment Variables

In the **Lambda → Configuration → Environment Variables** section, add the following:

| Variable              | Description                            |
| --------------------- | -------------------------------------- |
| `DYNAMODB_TABLE`      | Name of your DynamoDB table            |
| `SES_SENDER_EMAIL`    | Your verified sender email in SES      |
| `SES_RECIPIENT_EMAIL` | Email address to receive notifications |

---

### ⏱️ 7. Set Lambda Timeout

* Go to **Lambda → Configuration → General configuration**.
* Edit the timeout and increase it to **3–4 minutes** to allow for large receipt processing.

---

### 🔁 8. Configure S3 Event Trigger

* Go to your S3 bucket → **Properties** → **Event notifications**.
* Create a new event:

  * Event type: **Object Created (All)**
  * Destination: **Lambda Function**
  * Choose your Lambda function (e.g., `receiptProcessor`)

---

### ✅ 9. You’re All Set!

Upload a receipt image (JPG, PNG, or PDF) into the `receipts/` folder in your S3 bucket.
The Lambda function will automatically:

1. Extract data using Textract
2. Save it to DynamoDB
3. Send you an email summary via SES

## Enjoy your fully automated Receipt Tracker! 💼✨

Let me know if you'd like this as part of your final `README.md` or exported as a downloadable file.

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


