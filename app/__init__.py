from config import config
#celery
from celery import Celery
from flask import Flask,request,json,jsonify,Blueprint,send_from_directory
import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

celery = Celery(__name__)
celery.config_from_object('tasks.celeryconfig')

def create_app(config_name):
    app = Flask(__name__)
    
    # import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    
    # import module
    from app.api.testapi import testapi
    from app.api.test_add import test_add
    # register blueprint
    app.register_blueprint(testapi)
    app.register_blueprint(test_add)


    #######################################
    ##define log config and create log folder
    #######################################
    if os.path.isdir('log') == False:
        os.mkdir('log')
    if os.path.isfile('./log/flask.log') == False:
        with open("./log/flask.log",'w') as f:
            f.close()
    #====================================logging config======================================
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler("log/flask.log", when="D", interval=1, backupCount=15,encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    #====================================logging config======================================

    return app
    
