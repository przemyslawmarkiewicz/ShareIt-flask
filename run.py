from app import app, sess
import os

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

if __name__ == '__main__':
    
    
    app.run()
