import json
import os
import boto3
import uuid
from datetime import datetime
import urllib.parse

# Initialize AWS clients
s3 = boto3.client('s3')
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

# Get environment settings
DYNAMO_TABLE = os.getenv("DYNAMODB_TABLE", "my-reciept-db")
EMAIL_SENDER = os.getenv("SES_SENDER_EMAIL", "sender@example.com")
EMAIL_RECIPIENT = os.getenv("SES_RECIPIENT_EMAIL", "receiver@example.com")

def lambda_handler(event, context):
    try:
        # Extract bucket and object key from S3 event
        record = event["Records"][0]["s3"]
        bucket_name = record["bucket"]["name"]
        object_key = urllib.parse.unquote_plus(record["object"]["key"])

        # Confirm the file exists
        s3.head_object(Bucket=bucket_name, Key=object_key)

        # Analyze receipt using Textract
        receipt_info = analyze_receipt(bucket_name, object_key)

        # Store extracted info in DynamoDB
        save_to_dynamodb(receipt_info)

        # Send SES notification
        send_summary_email(receipt_info)

        return {
            "statusCode": 200,
            "body": json.dumps("Receipt processed successfully.")
        }

    except Exception as error:
        print(f"[ERROR] {error}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Failed to process receipt: {str(error)}")
        }

def analyze_receipt(bucket, key):
    """Extract details from a receipt using Textract's AnalyzeExpense API."""
    response = textract.analyze_expense(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )

    receipt_id = str(uuid.uuid4())
    today = datetime.utcnow().strftime("%Y-%m-%d")

    receipt = {
        "receipt_id": receipt_id,
        "date": today,
        "vendor": "Unknown",
        "total": "0.00",
        "items": [],
        "s3_path": f"s3://{bucket}/{key}"
    }

    docs = response.get("ExpenseDocuments", [])
    if not docs:
        return receipt

    summary = docs[0].get("SummaryFields", [])
    for field in summary:
        key_type = field.get("Type", {}).get("Text", "")
        val = field.get("ValueDetection", {}).get("Text", "")

        if key_type == "TOTAL":
            receipt["total"] = val
        elif key_type == "INVOICE_RECEIPT_DATE":
            receipt["date"] = val
        elif key_type == "VENDOR_NAME":
            receipt["vendor"] = val

    # Line items processing
    for group in docs[0].get("LineItemGroups", []):
        for entry in group.get("LineItems", []):
            item = {}
            for field in entry.get("LineItemExpenseFields", []):
                ftype = field.get("Type", {}).get("Text", "")
                fval = field.get("ValueDetection", {}).get("Text", "")
                if ftype == "ITEM":
                    item["name"] = fval
                elif ftype == "PRICE":
                    item["price"] = fval
                elif ftype == "QUANTITY":
                    item["quantity"] = fval
            if "name" in item:
                receipt["items"].append(item)

    return receipt

def save_to_dynamodb(data):
    """Insert parsed receipt data into DynamoDB."""
    table = dynamodb.Table(DYNAMO_TABLE)

    record = {
        "receipt_id": data["receipt_id"],
        "date": data["date"],
        "vendor": data["vendor"],
        "total": data["total"],
        "items": data["items"],
        "s3_path": data["s3_path"],
        "processed_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=record)
    print(f"Saved to DynamoDB: {data['receipt_id']}")

def send_summary_email(receipt):
    """Send formatted summary email using Amazon SES."""
    try:
        items_html = ""
        for item in receipt["items"]:
            items_html += f"<li>{item.get('name', 'Item')} - ${item.get('price', '0.00')} × {item.get('quantity', '1')}</li>"
        if not items_html:
            items_html = "<li>No items extracted</li>"

        body_html = f"""
        <html>
        <body>
            <h2>Receipt Summary</h2>
            <p><strong>Receipt ID:</strong> {receipt['receipt_id']}</p>
            <p><strong>Vendor:</strong> {receipt['vendor']}</p>
            <p><strong>Date:</strong> {receipt['date']}</p>
            <p><strong>Total:</strong> ${receipt['total']}</p>
            <p><strong>Stored At:</strong> {receipt['s3_path']}</p>
            <h3>Items</h3>
            <ul>{items_html}</ul>
        </body>
        </html>
        """

        ses.send_email(
            Source=EMAIL_SENDER,
            Destination={"ToAddresses": [EMAIL_RECIPIENT]},
            Message={
                "Subject": {"Data": f"Receipt Processed - {receipt['vendor']}"},
                "Body": {"Html": {"Data": body_html}}
            }
        )
        print("Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")
