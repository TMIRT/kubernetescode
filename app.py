from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        # VULNERABILITY PRESERVED: Direct execution of user input
        user_input = request.form.get('cmd')
        try:
            # DANGEROUS: os.popen allows shell command injection
            result = os.popen(user_input).read()
        except Exception as e:
            result = str(e)
        
    return render_template('index.html', user_input=user_input, cmd_output=cmd_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
