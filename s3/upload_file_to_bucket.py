import boto3
from botocore.client import Config

def upload_image_to_s3(file_path, file_name):
    """
        Upload image to s3 bucket.
        Args:
            file_path = image path from your local directory
            file_name = image file name saved from your pc
    """
	try:
		print ('Uploading image to s3 bucket')
		s3 = boto3.resource(
							's3',
							aws_access_key_id="aws_access_key",
							aws_secret_access_key="aws_secret_key",
							config=Config(signature_version='s3v4')
						)
		s3.meta.client.upload_file(file_path, 'bucket_name', file_name, ExtraArgs={"ContentType":'image/jpg', "ACL":'public-read'})
		print ('image uploaded')
	except OSError as ose:
		print (ose)