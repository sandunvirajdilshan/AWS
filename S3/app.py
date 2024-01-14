import boto3

# Create a Bucket
s3_resource = boto3.resource('s3')
s3_resource.create_bucket(
                Bucket='svd-test-bucket-001', 
                CreateBucketConfiguration={
                    'LocationConstraint': 'eu-north-1',
                },)
print("Bucket Created.,")


# List Objects in a Bucket
s3 = boto3.resource('s3')

bucket = s3.Bucket('svd-test-bucket-001')

response = bucket.objects.all()

for obj in response:
    print(obj.key)
