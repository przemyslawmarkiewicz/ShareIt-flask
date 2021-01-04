from app import app
import os

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
    
    
    app.run(debug=True)
