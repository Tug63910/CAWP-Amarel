#gs_utils contains functions to interact with google storage
from google.cloud import storage

def upload_blob(bucket_name,source_blob_name, destination_blob_name):
	
	storage_client=storage.Client()
	bucket=storage_client.bucket(bucket_name)
	blob=bucket.blob(destination_blob_name)

	blob.upload_from_string(source_blob_name)

def download_blob(bucket_name, source_blob_name):
	
	storage_client=storage.Client()
	bucket=storage_client.bucket(bucket_name)
	blob=bucket.blob(source_blob_name)
	text=blob.download_as_string()

	return text
