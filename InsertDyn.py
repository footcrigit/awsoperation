from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from flask import Flask, request
from flask_restful import Resource, Api
#from flask.ext.jsonpify import jsonify


app = Flask(__name__)
api = Api(app)
    
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class ReadfromDynamo(Resource):
    def get(self):
        dynamodb = boto3.resource("dynamodb", 
                                region_name='us-east-2', 
                                aws_access_key_id= "anything",
                                aws_secret_access_key= "anything",
                                endpoint_url="http://dynamodb.us-east-2.amazonaws.com")

        table = dynamodb.Table('MovieDetails')
        title = "slack"
        Movieid = 5

        try:
            response = table.put_item(
            Item ={
                'MovieID': Movieid,
                'Title': title
            }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            #item = response['Item']
            print("GetItem succeeded:")
            result = json.dumps(response, indent=4, cls=DecimalEncoder)
            return result

api.add_resource(ReadfromDynamo, '/putdata')
if __name__ == '__main__':
     app.run(port='8080')