from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')
    
@app.route('/add-item')
def add_tabe_item():
    return render_template('addItem.html')
    
@app.route('/update-item')
def update_table_item():
    return render_template('updateItem.html')
    
@app.route('/get-item')
def get_tabel_item():
    return render_template('getItem.html')
    
@app.route('/delete-item')
def delete_table_item():
    return render_template('deleteItem.html')
    
def navbar(message):
    return f"{render_template('navbar.html')}<br><br>{message}"


# Create table
@app.route('/create-table', methods=['POST'])
def create_table():
    
    table_name = request.form['tableName']
    partition_key = request.form['partitionKey']
    sort_key = request.form['sortKey']
    
    message = ""
    
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
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
    )
    
    
    message = f"Table {table_name} created successfully..,"
    
    return navbar(message)
        

# Add Item 
@app.route('/add-table-item', methods=['POST']) 
def add_item():
    table_name = request.form['tableName']
    reg_no = request.form['regNo']
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(table_name)
    
    item = {
        'regNo': reg_no,
        'name': name,
        'age': age,
        'address': address
    }
    
    response = table.put_item(Item=item)
    
    message =  'Successfully added the item..,'
    
    return navbar(message)


# Update item
@app.route('/update-table-item', methods=['POST'])
def update_item():
    table_name = request.form['tableName']
    reg_no = request.form['regNo']
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']

    if not table_name or not reg_no or not name:
        return 'Table Name, regNo, name are required..!'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    response = table.get_item(
        Key={
            'regNo' : reg_no,
            'name' : name,
        },
        AttributesToGet=[
        'name','age', 'address'
    ],
    )
    
    response_item = response['Item']

    if not age:
        new_age = response_item['age']
    else:
        new_age = age

    if not address:
        new_address = response_item['address']
    else:
        new_address = address

    response = table.update_item(
        Key={
            'regNo': reg_no,
            'name': name
        },
        UpdateExpression='SET age = :new_age, address = :new_address',
        ExpressionAttributeValues={
            ':new_age': new_age,
            ':new_address': new_address
        },
    )

    message =  'Successfully updated the item..,'
    
    return navbar(message)


# Get item
@app.route('/get-table-item')
def get_item_function():
    table_name = request.args.get('tableName')
    reg_no = request.args.get('regNo')
    name = request.args.get('name')

    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(table_name)
    
    response = table.get_item(
        Key={
            'regNo' : reg_no,
            'name' : name,
        },
        AttributesToGet=[
        'name','age', 'address'
    ],
    )
    
    item = response['Item']
    
    return navbar(item)


# Detele item 
@app.route('/delete-table-item')
def delete_item():
    table_name = request.args.get('tableName')
    reg_no = request.args.get('regNo')
    name = request.args.get('name')
    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(table_name)

    response = table.delete_item(
        Key={
            'regNo': reg_no,
            'name': name
        })
    
    message = 'Successfully deleted the item..,'
    
    return navbar(message)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')  