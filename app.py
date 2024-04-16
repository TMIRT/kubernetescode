from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello! Welcome to DevOps CI/CD Pipeline. This is build image #11 ---> http://ca91-1.winshipway.com/'
