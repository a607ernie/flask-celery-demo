from app.api import *

# BluePrint參數設定
testapi = Blueprint('testapi', __name__)

#API
@testapi.route('/testapi',methods=['GET'])
def testapi_m():
    try:
        return jsonify({"msg":"testapi OK"})
    except Exception as e:
        current_app.logger.warning(e,exc_info=True)
        return jsonify({"msg":"testapi fail"})