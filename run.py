from app import app
from app import init_db

if __name__=='__main__':
    init_db()
    app.run()
