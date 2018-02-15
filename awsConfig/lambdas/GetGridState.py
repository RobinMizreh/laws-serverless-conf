import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
    #dynamodb = boto3.resource("dynamodb", region_name='eu-west-1')
    client = boto3.client('dynamodb')
    try:
        response = client.get_item(
            TableName = 'Labyrinth',
            Key = {
                'key' : {
                    'S' : 'gridState',
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(response)
        return { 'grid': response["Item"]["grid"], 'pawn' : response["Item"]["pawn"], 'goalNb' : response["Item"]["goalNb"]}
