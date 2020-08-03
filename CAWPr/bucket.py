from os import environ

#Google Storage Bucket class
class GSbucket:
	def __init__(self):
		self.bucket=environ.get('GOOGLE_CLOUD_BUCKET')
		self.blob=environ.get('REMOTE_BLOB_NAME')


	
