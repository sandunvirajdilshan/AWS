from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')
    
@app.route("/put-item")
def add_item():
    return render_template('putItem.html')

# Create table
@app.route("/create-table", methods=['POST'])
def create_table():
    
    table_name = request.form['table_name']
    partition_key = request.form['partition_key']
    sort_key = request.form["sort_key"]
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': partition_key,
                    'KeyType': 'HASH' 
                },
                {
                    'AttributeName': sort_key,
                    'KeyType': 'RANGE' 
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': partition_key,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': sort_key,
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
    )
    
    table.wait_until_exists()
    
    return 'Table Created Successfully..!'
    

# Update table Item    
@app.route('/put-item', methods=["POST"]) 
def update_table_via_form():
    regNo = request.form['regNo']
    name = request.form['name']
    age = request.form['age']
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('StudentDetails')
    
    item = {
        'regNO':regNo,
        'name':name,
        'age': age
    }
    
    response = table.put_item(Item=item)
    
    return 'Successfully added the item.,'


# Get item from a table    
@app.route('/get-item')
def get_item():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('StudentDetails')
    
    response = table.get_item(
        Key={
            'regNO' : '002',
            'name' : 'Sandun Viraj',
        },
        AttributesToGet=[
        'name','age'
    ],
    )
    
    item = response['Item']
    
    return item


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')  
