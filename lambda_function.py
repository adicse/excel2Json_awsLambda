import os
import sys
import urllib.request
import boto3

import xlrd

print('Loading function')

debug_msgs = []


def lambda_handler(event, context):
    url = 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls'
    
    filename = fnDownloadFile( url )
    debug_msgs.append( 'downloaded: ' + filename )
    
    debug_msgs.append( 'creating json: ' + filename )
    sheetName = 'MICs List by CC'
    finalJson = fnParseXlsToJson(filename, sheetName)
    debug_msgs.append( '1 json entry: ' + str(finalJson[0]) )
    
    jsonFileName = filename + '.json'
    with open( jsonFileName, 'w' ) as fw:
        fw.write( str(finalJson ).replace("'", '"') )
        
    bucketName = 'test-adi-se-bucket'
    aws_s3 = aws('s3')
    aws_s3.fnGetBuckets( bucketName)
    debug_msgs.append( 'uploaded : ' + jsonFileName )
    aws_s3.fnUploadFile( bucketName, jsonFileName)
    return '\n     '.join( debug_msgs )
    #raise Exception('Something went wrong')
    
def fnDownloadFile( url, fname = ''):
    if fname == '':
        fname = '/tmp/' + url.rsplit('/',1)[-1]
    urllib.request.urlretrieve(url,  fname)
    return fname
    
def fnParseXlsToJson(path, sheetName):
    if not os.path.isfile( path ):
        print('File does not exist')
        return
    if sheetName is None:
        print('Please provide sheet name')
        return
        
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # get sheet names
    allSheets = book.sheet_names()
    if sheetName not in allSheets:
        print( sheetName , ' is not present in the file' )
        print( 'Available sheets are: ', allSheets )
        return
    
    # get the worksheet
    theSheet = book.sheet_by_index( allSheets.index( sheetName ) )
 
    # read 1st row
    header  = theSheet .row_values(0)
    finalJson = []
    for i in range(1, theSheet.nrows ):
        finalJson.append(   dict( zip(header, theSheet .row_values(i)) )   )
    return finalJson
    
class aws:
    def __init__(self, resClient):
        if resClient == 's3':
            # Create an S3 client
            print('Creating aws s3 client')
            self.s3 = boto3.client('s3')
        
    def fnGetBuckets(self, bucket, attempt = True ):
        # Call S3 to list current buckets
        response = self.s3.list_buckets()

        # Get a list of all bucket names from the response
        buckets = [bucket['Name'] for bucket in response['Buckets']]

        # Print out the bucket list
        if  bucket in buckets:
            print('Bucket found')
            debug_msgs.append( 'Bucket found: ' + bucket )
        elif attempt:
            self.fnCreateBucket(bucket)
        elif nattemp:
            debug_msgs.append( 'Bucket could not be created: ' + bucket )
            print('Bucket could not be created')
            sys.exit(0)
            
    def fnCreateBucket(self, bucketName):
        print('Creating aws bucket:', bucketName)
        debug_msgs.append( 'Creating aws bucket: ' + bucket )
        self.s3.create_bucket(Bucket=bucketName)
        self.fnGetBuckets( bucketName , False)
        
    def fnUploadFile(self, bucketName = '' , fileName = ''):
        if fileName == '':
            print('Kindly provide file name to upload')
            return False
        if bucketName == '':
            print('Kindly provide file bucketName to upload into')
            return False
        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        debug_msgs.append( 'uploading file aws bucket: ' + fileName )
        self.s3.upload_file(fileName, bucketName, os.path.split( fileName)[-1] ) 
        
        