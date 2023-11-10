import json
import boto3


ACCESS_KEY = 'AKIA6I5TH4GFJP7Y7PVX'
SECRET_KEY = 'zrjD1s MetIDwj1sbZ2BuP85zrywxJSO0UioUSah'
#To get the table object from DynamoDB
#To get the table object from DynamoDB
#To get the table object from DynamoDB
#To get the table object from DynamoDB
#pokemon louco
def getTable(table_name, ACCESS_KEY, SECRET_KEY):
	session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key= SECRET_KEY)
#Create a DynamoDB resource
	dynamoDB = session.resource('dynamodb', region_name= 'us-east-1')
	pokemon_table = dynamoDB.Table(table_name)
	return pokemon_table
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key= SECRET_KEY,
region_name = 'us-east-1')
def lambda_handler(event, context):
	try:
#Result variable to capture whether data has been loaded or not
		data_loaded = False
#Fetch bucket and key information from the event object
		bucket_name = event['Records'][0]['s3']['bucket']
		key = event['Records'][0]['s3']['object']['key']
#Read the data from the s3 file
		json_data = s3_client.get_object(Bucket = 'infnetatividade2', Key = 'pokemon.json')
		pokemon_data = json.loads(json_data['Body'].read())
#Get the dynamo db table where we want to populate our data
		pokemon_table = getTable("pokemon", ACCESS_KEY, SECRET_KEY)
		for data in pokemon_data:
#Fetch only the required information
			id = data['id']
			name = data['name']['english']
			type = data['type'][0]
#Insert the data point into the table
			pokemon_table.put_item(Item = {'id' : id, 'name':name, 'type': type})
		data_loaded = True
	except Exception as e:
		print(event)
		print(e)
	finally:
		return data_loaded