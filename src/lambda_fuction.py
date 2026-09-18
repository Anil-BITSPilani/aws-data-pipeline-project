import json
import boto3
import csv
import os
from datetime import datetime

# Initialize AWS SDK Clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileProcessingMetadata')

def lambda_handler(event, context):
    # Log incoming event structured payload
    print("Received event: " + json.dumps(event, indent=2))
    
    try:
        # Extract bucket name and file key from S3 Event payload
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        file_size = record['s3']['object']['size']
        
        # Download the file to local ephemeral storage /tmp space
        local_filename = '/tmp/' + os.path.basename(file_key)
        s3_client.download_file(bucket_name, file_key, local_filename)
        
        # Read and parse CSV safely to handle special encodings (prevent UnicodeDecodeError)
        row_count = 0
        column_count = 0
        
        with open(local_filename, mode='r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader, None)
            if header:
                column_count = len(header)
                row_count += 1  # Include header if it counts as a row, or keep track of data lines
            for row in csv_reader:
                row_count += 1

        # Extract file extension/type
        _, file_extension = os.path.splitext(file_key)
        
        # Construct DynamoDB structured JSON payload
        item_payload = {
            'file_name': file_key,
            'columns': column_count,
            'file_size_bytes': file_size,
            'file_type': file_extension if file_extension else '.csv',
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Concurrently execute put_item to Amazon DynamoDB
        table.put_item(Item=item_payload)
        
        # Log out strict string output metrics targeted by CloudWatch logs parsing
        metrics_log = f'Processed File Metrics: {json.dumps(item_payload)}'
        print(metrics_log)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Pipeline execution completed successfully!')
        }
        
    except Exception as e:
        print(f"[ERROR] Pipeline Execution Failure: {str(e)}")
        raise e
