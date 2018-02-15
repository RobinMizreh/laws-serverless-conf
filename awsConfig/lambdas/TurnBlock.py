import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
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
        gridState = json.loads(response["Item"]["grid"]["S"])
        pawn = json.loads(response["Item"]["pawn"]["S"])
        goalNb = json.loads(response["Item"]["goalNb"]["N"])
        x = int(event['x'])
        y = int(event['y'])
        gridState[x][y] = (gridState[x][y] + 1) % 4
        print(gridState)
        try:
            client.put_item(
                TableName = 'Labyrinth',
                Item={
                    'key' : {
                        'S' : 'gridState',
                    },
                    'grid' : {
                        'S' : json.dumps(gridState),
                    },
                    'pawn' : {
                        'S' : json.dumps(pawn),
                    },
                    'goalNb' : {
                        'N' : json.dumps(goalNb),
                    },
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return null
        else:
            return { 'grid': { 'S' : json.dumps(gridState)}, 'pawn' : response["Item"]["pawn"], 'goalNb' : response["Item"]["goalNb"] }
