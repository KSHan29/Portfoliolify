from app import app, socketio

@app.route('/')
def index():
    return 'Hello, World!'

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
