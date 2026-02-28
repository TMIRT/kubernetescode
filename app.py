from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    cmd_output = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_text', '')
        
        # VULNERABILITY: Directly concatenating user input into a shell command
        # A legitimate use would be 'ping -c 1 google.com'
        # An exploit would be 'google.com; cat /etc/passwd'
        try:
            command = f"ping -c 1 {user_input}"
            cmd_output = os.popen(command).read()
        except Exception as e:
            cmd_output = str(e)
        
    return render_template('index.html', user_input=user_input, cmd_output=cmd_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
