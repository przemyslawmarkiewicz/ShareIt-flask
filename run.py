from app import app, sess
import os

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.urandom(24)

sess.init_app(app)


if __name__ == '__main__':
    
    
    app.run()
