from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello! Welcome to DevOps CI/CD Pipeline. This is build image revision #37(a)'
