import json
import json
import base64
import boto3
from requests_toolbelt.multipart import decoder
import traceback

s3client = boto3.client("s3")


def upload_to_s3(lst, name):
    response = s3client.put_object(Body=lst[0].encode(
        'iso-8859-1'), Bucket='rahul-project-bucket', Key=name)
    print(response)


def version_4(event):
    content_type_header = event['headers']['content-type']
    postdata = base64.b64decode(event['body']).decode('iso-8859-1')
    lst = []
    for part in decoder.MultipartDecoder(postdata.encode('utf-8'), content_type_header).parts:
        lst.append(part.text)
    upload_to_s3(lst, "image.jpeg")


def handler(event, context):
    print(event)
    try:
        version_4(event)
        response = {
            "statusCode": 200,
            "body": "Success",
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
        }
        return response

    except Exception as error:
        print("error")
        body = str(error)
        print(body)
        traceback.print_exception(
            type(error), value=error, tb=error.__traceback__)
        return {
            "statusCode": 500,
            "body": body,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
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
