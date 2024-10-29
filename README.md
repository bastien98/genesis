# Requirements
Python v3.11 <br>
Poetry <br>
Mysql server <br>
Postman <br>

## Installation

Create a new python virtual env with python 3.11

### Initialize Mysql database
1) Start Mysql server (MacOS): <br>
`brew services start mysql `
2) Run database init script
3) `mysql -u root < path/to/init_mysql_database.sql`

### Install packages
1) Run: `poetry install`
2) Run: `pip install llama-parse`

### Test Installation
1) Start the application: <br>
`cd path/to/super-rag/api/src` <br>
Run: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`<br>
2) Test with postman request and dummy pdf file: <br>
POST http://0.0.0.0:8000/v2/knowledge_bases/1/documents/add?user_id=1 <br>
add pdf file to body of the request: <br>
Key: document, type File <br>
Value: sample.pdf
3) Run request <br>
Expected output: `{
    "message": "Document uploaded and processed successfully.",
    "document": "sample.pdf"
}`




