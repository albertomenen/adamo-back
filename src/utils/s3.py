import base64
import boto3
from botocore.exceptions import NoCredentialsError
from ..config import S3_Credentials

bucket = S3_Credentials.get('BUCKET')
s3 = boto3.resource('s3', aws_access_key_id=S3_Credentials.get('ACCESS_KEY'),
                    aws_secret_access_key=S3_Credentials.get('SECRET_KEY'))


def upload_to_aws(data, s3_filename):
    try:
        base64.b64decode(data)
        new_object = s3.Object(bucket, s3_filename)
        new_object.put(Body=data)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except:
        return False


def get_from_aws(s3_filename, to_base64=False):
    result = s3.Bucket(bucket).Object(s3_filename).get()
    if result and result.get('Body'):
        result = base64.b64encode(result.get('Body').read()) if to_base64 else result.get('Body').read()
        try:
            return result.decode('ascii')
        except:
            raise Exception('Cant download image')
    else:
        return None
