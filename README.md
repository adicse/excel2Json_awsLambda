Requirements
    Lambda Role: ( full access not mandatory but for time saving provided full access )
        AWSLambdaFullAccess
        AmazonS3FullAccess
        AWSLambdaExecute
        
    timeout: ( always good to have buffer :) 
        10 seconds: default is 3, it takes a little more than 3 seconds
        
Rest things were at default for hello_world python 3.6

The code requires, sheet name, bucket name ( to which json will be uploaded )

Kindly provide an existing bucket with required permissions.

if bucket is not present it will try to create the bucket,


Kindly upload the .zip file as it is to lamda function,

handler:  lambda_function.lambda_handler



Sample  log

Response:
"downloaded: /tmp/ISO10383_MIC.xls
creating json: /tmp/ISO10383_MIC.xls
1 json entry: {'ISO COUNTRY CODE (ISO 3166)': 'AE', 'COUNTRY': 'UNITED ARAB EMIRATES', 'MIC': 'DGCX', 'OPERATING MIC': 'DGCX', 'O/S': 'O', 'NAME-INSTITUTION DESCRIPTION': 'DUBAI GOLD & COMMODITIES EXCHANGE DMCC', 'ACRONYM': 'DGCX', 'CITY': 'DUBAI', 'WEBSITE': 'WWW.DGCX.AE', 'STATUS DATE': 'DECEMBER 2005', 'STATUS': 'ACTIVE', 'CREATION DATE': 'DECEMBER 2005', 'COMMENTS': ''}\n     
Bucket found: test-adi-se-bucket\n     
uploaded : /tmp/ISO10383_MIC.xls.json\n     
uploading file aws bucket: /tmp/ISO10383_MIC.xls.json"

Request ID:
"e5a15172-779f-11e8-a08b-bfddca51ab15"

Function Logs:
START RequestId: e5a15172-779f-11e8-a08b-bfddca51ab15 Version: $LATEST
Creating aws s3 client
Bucket found
END RequestId: e5a15172-779f-11e8-a08b-bfddca51ab15
REPORT RequestId: e5a15172-779f-11e8-a08b-bfddca51ab15	Duration: 3879.08 ms	Billed Duration: 3900 ms 	Memory Size: 128 MB	Max Memory Used: 40 MB	