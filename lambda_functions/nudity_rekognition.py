
import boto3
from botocore.client import Config


def moderate_image(event, context):
    """
        Amazon rekognition. Check if image contains Explicit Nudity or Nudity.
        Return : 
                0 = no nudity detected
                1 = positive for nudity
                2 = cannot find image file in s3
		Sample returns from manual checking so far. 
		Explicit Nudity : Illustrated Explicit Nudity, Graphic Male Nudity, Nudity
	"""
	image = event['file_name']
	client = boto3.client('rekognition')
	try:
		response = client.detect_moderation_labels(Image={'S3Object':{'Bucket':'bucket_name', 'Name':image}})
		print('Detected labels for ' + image)  
		print('Detecting image if contains nudity')  
		for label in response['ModerationLabels']:
			print (label['Name'] + ' : ' + str(label['Confidence']))
			print (label['ParentName'])
			label_names = [label['Name'], label['ParentName']]
			if 'nudity' in ','.join(label_names).lower():
				print ('positive for nudity')
				return 1
		print ('negative for nudity')
		return 0
	except client.exceptions.InvalidS3ObjectException as no_file:
		print ('Cannot find ', image, ' in s3 bucket')
		return 2
