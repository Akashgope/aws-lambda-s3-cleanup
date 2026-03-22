import boto3
from datetime import datetime, timezone, timedelta


# Configuration
BUCKET_NAME = 'my-cleanup-bucket-2026'   # Your bucket name
# For final assignment: DAYS_THRESHOLD = 30
# For quick testing: set DAYS_THRESHOLD = 0.003 (≈4.32 minutes) or 0.0007 (≈1 minute)
DAYS_THRESHOLD =  0.003                       # Change to 0.003 for testing (5 minutes approx.)


def lambda_handler(event, context):
   s3 = boto3.client('s3')
   try:
       # List all objects in the bucket
       response = s3.list_objects_v2(Bucket=BUCKET_NAME)
       if 'Contents' not in response:
           print(f"No objects found in bucket {BUCKET_NAME}.")
           return {'statusCode': 200, 'body': 'No objects found'}
      
       # Calculate cutoff date (UTC)
       cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_THRESHOLD)
       deleted_objects = []


       for obj in response['Contents']:
           last_modified = obj['LastModified']
           if last_modified < cutoff_date:
               # Delete the object
               s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
               deleted_objects.append(obj['Key'])
               print(f"Deleted: {obj['Key']} (LastModified: {last_modified})")
           else:
               print(f"Kept: {obj['Key']} (LastModified: {last_modified})")


       print(f"Total deleted: {len(deleted_objects)}")
       return {
           'statusCode': 200,
           'body': f"Deleted {len(deleted_objects)} objects"
       }
   except Exception as e:
       print(f"Error: {e}")
       raise