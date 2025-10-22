import boto3
from botocore.exceptions import ClientError
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class S3Manager:
    """
    Manages file uploads to DigitalOcean Spaces (S3-compatible)
    """
    
    def __init__(self):
        """
        Initialize S3 client for DigitalOcean Spaces
        """
        self.access_key = os.getenv("DO_SPACES_KEY")
        self.secret_key = os.getenv("DO_SPACES_SECRET")
        self.endpoint_url = os.getenv("DO_SPACES_ENDPOINT")
        self.bucket_name = os.getenv("DO_SPACES_BUCKET")
        self.region = os.getenv("DO_SPACES_REGION", "fra1")
        
        if not all([self.access_key, self.secret_key, self.endpoint_url, self.bucket_name]):
            raise ValueError("DigitalOcean Spaces credentials should already be in the real .env using the example file")
        
        logger.info(f"Initializing S3 client for bucket: {self.bucket_name}")
        
        try:
            # Initialize boto3 client for DigitalOcean Spaces
            self.client = boto3.client(
                's3',
                region_name=self.region,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
            
            logger.info("S3 client initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing S3 client: {str(e)}")
            raise
    
    def upload_file(self, file_content: bytes, filename: str) -> str:
        """
        Upload file to DigitalOcean Spaces
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Public URL of the uploaded file
        """
        try:
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            
            logger.info(f"Uploading file: {unique_filename}")
            
            # Upload file
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ACL='public-read'  # publicly accessible
            )
            
            # Construct public URL
            # Format: https://bucket-name.region.digitaloceanspaces.com/filename
            base_url = self.endpoint_url.replace('https://', '')
            public_url = f"https://{self.bucket_name}.{base_url}/{unique_filename}"
            
            logger.info(f"File uploaded successfully: {public_url}")
            return public_url
        
        except ClientError as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete file from DigitalOcean Spaces
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Deleting file: {filename}")
            
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            
            logger.info("File deleted successfully")
            return True
        
        except ClientError as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def list_files(self) -> list:
        """
        List all files in the bucket
        
        Returns:
            List of file keys
        """
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name)
            
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                return []
        
        except ClientError as e:
            logger.error(f"Error listing files: {str(e)}")
            return []