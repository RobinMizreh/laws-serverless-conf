import boto3
import json
from botocore.exceptions import ClientError
from random import randint

mapContent = [
  [1,1,1,2,0,1,1],
  [2,0,2,0,2,1,0],
  [1,1,0,1,0,2,0],
  [0,1,2,0,1,0,2],
  [0,1,2,0,1,2,1],
  [2,1,1,0,2,1,0],
  [1,0,2,1,0,0,1],
]

tilesByPaths = [
  ['00', '02', '03', '12', '13', '20', '22'],
  ['00', '01', '03', '10', '13', '21', '23'],
  ['00', '01', '02', '10', '11', '20', '22'],
  ['01', '02', '03', '11', '12', '21', '23'],
]

icons = [
  [0, 0, 1, 2, 3, 3, 4, 5, 6, 6],
  [3, 6, 1, 5, 2, 6, 4, 0, 3, 4],
]

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
        begin = json.loads(event['begin'])
        end = json.loads(event['end'])
        direction = getDirection(begin, end)
        newPos = begin
        if (begin == pawn and isValidPath(begin, end, direction, gridState)) :
        #if (isValidPath(begin, end, direction, gridState)) :
            print('Moving !')
            newPos = end
            print(newPos)
            goalNb = changeGoalIfNeeded(newPos, goalNb)
            try:
                print(newPos)
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
                            'S' : json.dumps(newPos),
                        },
                        'goalNb' : {
                            'N' : json.dumps(goalNb),
                        }
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
                return null
            else:
                return { 'grid': { 'S' : json.dumps(gridState)}, 'pawn' : {'S' : json.dumps(newPos)}, 'goalNb' : {'N' : json.dumps(goalNb)} }
        else:
            return { 'grid': { 'S' : json.dumps(gridState)}, 'pawn' : {'S' : json.dumps(newPos)}, 'goalNb' : {'N' : json.dumps(goalNb)} }

def getDirection(begin, end):
    if (begin[0] == end[0]):
        if (begin[1] > end[1]):
            return 0
        else:
            return 2
    else:
        if (begin[0] > end[0]):
            return 3
        else:
            return 1

def isValidPath(begin, end, direction, gridState):
    if (end[0] >= 0 and end[0] < 7 and end[1] >= 0 and end[1] < 7):
        if (isWay(begin, direction, gridState) and isWay(end, (direction+2)%4, gridState)):
            return True
        else:
            return False
    else:
        return False

def isWay(cell, direction, gridState):
    code = str(mapContent[cell[0]][cell[1]]) + str(gridState[cell[0]][cell[1]])
    return (code in tilesByPaths[direction])

def changeGoalIfNeeded(newPos, goalNb):
    if (newPos[0] == icons[0][goalNb] and newPos[1] == icons[1][goalNb]):
        print("Touch !")
        newGoal = goalNb
        while(newGoal == goalNb):
            newGoal = randint(0, len(icons[0])-1)
        goalNb = newGoal
    return goalNb
