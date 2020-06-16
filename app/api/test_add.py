from app.api import *

from tasks.add import add
# BluePrint參數設定
test_add = Blueprint('test_add', __name__)

#API
@test_add.route('/test_add',methods=['GET'])
def test_add_m():
    try:
        res = add.delay(12,23)
        return jsonify({"STATUS":res.state,"RESULT":res.get()})
    except Exception as e:
        current_app.logger.warning(e,exc_info=True)
        return jsonify({"msg":"add fail"})