import boto3

s3 = boto3.resource('s3')

bucket = s3.Bucket('pythontestbucket-sandun-002')

response = bucket.objects.all()

for obj in response:
    print(obj.key)
