from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/create-table", methods=['POST'])
def create_table():
    
    table_name = request.form['table_name']
    partition_key = request.form['partition_key']
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': partition_key,
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                'AttributeName': partition_key,
                'KeyType': 'HASH'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
                }
            )
    
    table.wait_until_exists()
    
    return '<h1>Table Created..!</h1>'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')  