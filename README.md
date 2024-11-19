
# **Facebook Lead Ads Webhook Integration**

This project provides an integration between **Facebook Lead Ads** and **AWS Lambda**, enabling you to securely capture lead data, store it in an **S3 bucket**, and forward it to a specified webhook URL.

---

## **Features**

- **Webhook Integration:** Receives lead data from Facebook via a secure webhook.
- **S3 Storage:** Stores lead data in an S3 bucket with a structured folder hierarchy (`ClientName/Year/Month/Day/LeadID.json`).
- **Data Forwarding:** Forwards lead data (`changes` dictionary) to a specified webhook URL.
- **Scalable and Secure:** Uses AWS Lambda's serverless architecture with environment variables for security.

---

## **Architecture Overview**

1. **Facebook Webhook:** Facebook sends lead data to the Lambda function via a webhook.
2. **AWS Lambda:**
   - Processes the incoming data.
   - Saves the data to S3 in a structured format.
   - Forwards specific data (`changes` dictionary) to a configured webhook URL.
3. **Webhook Destination:** The final recipient processes the forwarded data.

---

## **Prerequisites**

Before you begin, ensure you have the following:

1. **AWS Account:**
   - Access to AWS Lambda and S3.
2. **Facebook Developer Account:**
   - A Facebook app with Lead Ads enabled.
3. **Python 3.9+**
4. **Environment Configuration:**
   - `BUCKET_NAME`: Your S3 bucket name.
   - `DESTINATION_URL`: The URL to forward lead data.
   - `VERIFY_TOKEN`: Token used to validate Facebook's webhook.

---

## **Setup and Deployment**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### **2. Configure Environment Variables**
In the AWS Lambda console, configure the following environment variables:

| Variable        | Description                                  | Example                      |
|------------------|----------------------------------------------|------------------------------|
| `BUCKET_NAME`   | Name of the S3 bucket to store lead data.    | `my-s3-bucket-name`          |
| `DESTINATION_URL` | URL to forward the lead data.              | `https://example.com/webhook`|
| `VERIFY_TOKEN`  | Token for Facebook webhook verification.     | `my-secret-verify-token`     |

### **3. Deploy the Lambda Function**
1. Zip the project folder:
   ```bash
   zip -r lambda_function.zip .
   ```
2. Upload the zip file to AWS Lambda.

### **4. Set Up Facebook Webhook**
1. Go to the **Facebook Developer Console** > **Your App** > **Webhooks**.
2. Add a new webhook subscription:
   - **Callback URL:** Your API Gateway URL (e.g., `https://your-api-id.amazonaws.com/your-stage-name/facebook_webhook`).
   - **Verify Token:** The same value as `VERIFY_TOKEN`.
3. Subscribe to the **Lead Ads** topic.

---

## **Folder Structure**

```
/project-root
  ├── lambda_function.py         # Main Lambda function code
  ├── requirements.txt           # List of dependencies
  ├── README.md                  # Project documentation
  ├── .gitignore                 # Files to exclude from GitHub
```

---

## **How to Test**

1. **Facebook Lead Ads Testing Tool:**
   - Use the testing tool in the Facebook Developer Console to submit test leads.
2. **S3 Verification:**
   - Check the S3 bucket to confirm data is stored in the correct folder structure.
3. **Webhook Destination:**
   - Monitor the destination URL to verify the forwarded data.

---

## **S3 Folder Structure Example**

```
/Test/2024/11/04/444444444444.json
```

- **`Test`**: Client name (mapped from `page_id`).
- **`2024/11/04`**: Date the lead was created.
- **`444444444444.json`**: Lead ID.

---

## **Error Handling**

1. **Invalid Event Structure:**
   - Returns a `400` error with details logged in CloudWatch.
2. **Forwarding Errors:**
   - Logs forwarding issues, including response codes and error details.
3. **Missing Request Body:**
   - Returns a `400` error if the webhook request lacks a body.

---

## **License**

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this project as long as you retain the original license.

---

## **Contributing**

Contributions are welcome! Please fork the repository and create a pull request with your changes.
