import json
from cgi import parse_header, parse_multipart
from io import BytesIO

"""

{
  body: "file contents"
}

"""

def handler(event, context):
    try: 
      body = {
          "message": "Go Serverless v1.0! Your function executed successfully!",
          "input": event
      }

      file_contents = event["body"]
      print(file_contents)

      try: 
        c_type, c_data = parse_header(event['headers']['Content-Type'])
        assert c_type == 'multipart/form-data'
        form_data = parse_multipart(BytesIO(event['body'].decode('base64')), c_data)
        uploaded_file = form_data.files['file']
        print(uploaded_file)
        filename = uploaded_file.filename
        print(filename)
      except Exception as error: 
        print(error)
        
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
        return {
            "statusCode": 500,
            "body": str(error.val), 
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
