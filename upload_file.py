import json
import json
import base64
import boto3
from requests_toolbelt.multipart import decoder
import traceback

s3client = boto3.client("s3")

def version_1(event): 
  content_type_header = event['headers']['content-type']
  postdata = base64.b64decode(event['body']).decode('iso-8859-1')
  lst = []
  for part in decoder.MultipartDecoder(postdata.encode('utf-8'), content_type_header).parts:
    lst.append(part.text)
  response = s3client.put_object(Body=lst[0].encode('iso-8859-1'),  Bucket='rahul-project-bucket',    Key='mypicturefinal.jpeg')
  print(response)


def version_2(event):
  # fileName = "random.jpeg"
  bodyData = event['body']
  decodedFile = base64.b64decode(bodyData).decode('iso-8859-1')
  # print(decodedFile.headers)
  lst = []
  for part in decoder.MultipartDecoder(decodedFile, event['headers']['content-type']).parts:
    lst.append(part.text)
  response = s3client.put_object(Body=lst[0].encode('iso-8859-1'),  Bucket='rahul-project-bucket',    Key='mypicturefinal.jpeg')
  print(response)
  # s3client.put_object(Bucket='rahul-project-bucket', Key=fileName, Body=decodedFile.content)


def version_4(event): 
  content_type_header = event['headers']['content-type']
  postdata = base64.b64decode(event['body']).decode('iso-8859-1')
  lst = []
  for part in decoder.MultipartDecoder(postdata.encode('utf-8'), content_type_header).parts:
      lst.append(part.text)
  response = s3client.put_object(Body=lst[0].encode('iso-8859-1'),Bucket='rahul-project-bucket', Key='mypicturefinal.jpg')
  print(response)

def version_3(event): 
  from cgi import parse_header, parse_multipart
  from io import BytesIO
  form_data = parse_multipart(BytesIO(event['body'].decode('base64')))
  uploaded_file = form_data.files['file']
  print(uploaded_file)
  filename = uploaded_file.filename
  print(filename)

def handler(event, context):
  print(event)
  try:  
    version_4(event)
    response = {
        "statusCode": 200,
        "body": "Success", 
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials':True, 
        },
    }
    return response
  
  except Exception as error: 
    print("error")
    body = str(error)
    print(body)
    traceback.print_exception(type(error), value=error, tb=error.__traceback__)
    return {
        "statusCode": 500,
        "body": body, 
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials':True, 
        },
    }
  

  # Use this code if you don't use the http event with the LAMBDA-PROXY
  # integration
  """
  return {
      "message": "Go Serverless v1.0! Your function executed successfully!",
      "event": event
  }
  """
