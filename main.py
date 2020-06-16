# import module 
from app import *

from tasks.add import add

app = create_app('default')


@app.route('/')
def index():
    return "Hello World"

@app.route('/error')
def error_m():
    app.logger.info('info log')
    try:
        raise
    except Exception as e:
        app.logger.warning(e,exc_info=True)
    return "Write error log"


@app.route('/get_route_map',methods=['GET'])
def getroutemap():
    return str(app.url_map)



if __name__ == '__main__':
    app.run(app.config['HOST'],app.config['PORT'],app.config['DEBUG'])
