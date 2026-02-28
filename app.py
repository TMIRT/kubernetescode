from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cmd_output = None
    user_input = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_text', '')
        
        try:
            # shell=True allows execution of any shell string/piping
            # stderr=subprocess.STDOUT ensures we see error messages too
            cmd_output = subprocess.check_output(
                user_input, 
                shell=True, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            cmd_output = e.output
        except Exception as e:
            cmd_output = str(e)
        
    return render_template('index.html', user_input=user_input, cmd_output=cmd_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
