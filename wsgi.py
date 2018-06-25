from flask import Flask
from app import create_app
import app.error_class

application = create_app()

if __name__ == '__main__':
    application.run()
