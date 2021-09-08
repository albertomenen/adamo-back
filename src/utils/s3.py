import base64
import boto3
from botocore.exceptions import NoCredentialsError
from ..config import S3_Credentials

bucket = S3_Credentials.get('BUCKET')
s3 = boto3.client('s3', aws_access_key_id=S3_Credentials.get('ACCESS_KEY'),
                  aws_secret_access_key=S3_Credentials.get('SECRET_KEY'))


def upload_to_aws(data, s3_filename, from_base64=False):
    try:
        data = base64.b64decode(data) if from_base64 else data
        new_object = s3.Object(bucket, s3_filename)
        new_object.put(Body=data)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


def get_from_aws(s3_filename, to_base64=False):
    result = s3.Bucket(bucket).Object(s3_filename).get()
    if result and result.get('Body'):
        result = base64.b64encode(result.get('Body').read()) if to_base64 else result.get('Body').read()
    else:
        return None
    return result

