# S3 Bulk File Upload (with last-modified metadata)
A Simple script to upload files in a directory to an S3 bucket. 


The script also sets the `last-modified` metadata attribute for each file, 
since the file's created date is not retained when the object is uploaded.

## Example usage
```
python main.py 'D:\Pictures\iphone photos 06-07-19' my-bucket my-folder
```