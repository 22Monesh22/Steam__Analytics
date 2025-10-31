from flask import Flask, render_template

app = Flask(__name__)

@app.route('/test-login')
def test_login():
    return render_template('auth/login.html')

@app.route('/test-register') 
def test_register():
    return render_template('auth/register.html')

if __name__ == '__main__':
    print("Testing templates on port 5001...")
    app.run(debug=True, port=5001)