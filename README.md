# S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective
Automatically delete files older than 30 days from an S3 bucket.

## Steps Followed

### 1. S3 Setup
- Created a bucket named `my-cleanup-bucket-2026` in `ap-south-1` (Mumbai) region.
- Uploaded several test files (`file1.txt`, `file2.txt`, `file3.txt`) to the bucket.

**Screenshot:**  
<img width="1662" height="663" alt="Screenshot 2026-03-22 at 3 36 20 PM" src="https://github.com/user-attachments/assets/2f04875b-c144-4a4b-9b25-4bbc4fe19603" />


### 2. IAM Role for Lambda
- Created a role named `LambdaS3CleanupRole`.
- Attached policies:
  - `AmazonS3FullAccess` – to list, read, and delete objects.
  - `AWSLambdaBasicExecutionRole` – to write logs to CloudWatch.

**Screenshot:**  
<img width="1680" height="870" alt="Screenshot 2026-03-22 at 3 37 06 PM" src="https://github.com/user-attachments/assets/386e6291-354f-413f-a5da-22b57801ebc1" />


### 3. Lambda Function
- Runtime: Python 3.x.
- Timeout set to 1 minute (to allow enough time for listing and deleting).
- Code: `lambda_function.py` (see repository).
- The function lists all objects in the bucket, compares `LastModified` with a cutoff date, and deletes those older than the threshold.

**Screenshot:**  
<img width="1376" height="859" alt="Screenshot 2026-03-22 at 3 47 56 PM" src="https://github.com/user-attachments/assets/990d6f79-0d97-4723-9534-daf5c33266dd" />


### 4. Testing with a Shorter Threshold
Because I didn’t have files older than 30 days, I temporarily changed the `DAYS_THRESHOLD` to `0.003` (approximately 5 minutes). This allowed me to verify that files uploaded earlier were correctly identified and deleted.

After confirming the logic worked, I set the threshold back to `30` days for the final code. The function now deletes files older than 30 days.

**Screenshot:**  
<img width="1680" height="524" alt="Screenshot 2026-03-22 at 3 34 36 PM" src="https://github.com/user-attachments/assets/e8555492-9fea-4c97-b272-d71320711602" />

<img width="1391" height="871" alt="Screenshot 2026-03-22 at 3 49 35 PM" src="https://github.com/user-attachments/assets/a1d3de4b-c316-43a8-b3e7-718543793764" />


### 5. Verification
- After running the Lambda with the 5‑minute threshold, the older files were removed from the bucket.


**Screenshot:**  
<img width="1665" height="507" alt="Screenshot 2026-03-22 at 3 51 05 PM" src="https://github.com/user-attachments/assets/b54b16cf-7084-4920-8502-d1b5e440cc06" />


## Code
The Lambda function code is available in [`lambda_function.py`](lambda_function.py).

## Conclusion
The function successfully deletes objects older than the specified threshold. By using a short threshold for testing, I confirmed the logic works correctly. This automation can be used for regular cleanup tasks in S3 buckets.
