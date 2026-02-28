from flask import Flask, render_template, request, html_escape

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    if request.method == 'POST':
        # Get the input from the form
        user_input = request.form.get('user_text', '')
        
    return render_template('index.html', user_input=user_input)

if __name__ == '__main__':
    # Listen on all interfaces for container compatibility
    app.run(host='0.0.0.0', port=5000, debug=False)
