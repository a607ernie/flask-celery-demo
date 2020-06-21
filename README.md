Flask Celery
===

## Index
- [Flask Celery](#flask-celery)
  - [Index](#index)
  - [Celery 簡介](#celery-簡介)
    - [什麼是Celery](#什麼是celery)
  - [環境架設](#環境架設)
    - [建立Flask Server](#建立flask-server)
    - [新增API](#新增api)
    - [建立 Celery Worker](#建立-celery-worker)
    - [建立一個task](#建立一個task)
    - [建立 celery config](#建立-celery-config)
    - [RUN](#run)
  - [Request Test](#request-test)
  - [定時任務](#定時任務)
  - [加上定時任務後，再次測試](#加上定時任務後再次測試)
  - [Flower 監控](#flower-監控)
  - [END](#end)


Celery 簡介
---
### 什麼是Celery
Celery 是一個非同步的任務佇列，他簡單、靈活、可靠，是一個專注於及時處理的任務佇列。

Celery包含threads/process pool。通常是將任何需要消耗資源的任務放到佇列中，讓Flask可以正常回應客戶端的請求，而不會被某些請求卡住。

Celery具有三個核心元件:

1. Celery用戶端: 負責發布後端作業。與Flask一起運行
2. Celery workers : 這些是負責執行作業的執行緒。可以在Flask上啟動單獨的worker，或是之後可以依據需求增加更多的worker。
3. 訊息代理: 客戶端透過訊息佇列和workers進行溝通，Celery可以使用多種方式來實作這些佇列。最常用的是**RabbitMQ**和**Redis**

環境架設
---
首先安裝好python3.7.x的版本，用pip安裝```virtualenv```，並進入虛擬環境中
```
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
```

安裝需要用到的packages:

```bash
$ pip install flask
$ pip install celery
$ pip install flower
$ pip install redis
```


或是使用```requirements.txt```去安裝
```
$ pip install -r requirements.txt
```

### 建立Flask Server

這邊為了整體架構完整，以及方便增加Blueprint

因此把main中宣告```app=Flask(__name__)```這塊移到```app.__init__.py```


```python
#main.py
from app import *
app = create_app('default')
@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(app.config['HOST'],app.config['PORT'],app.config['DEBUG'])
```

在create_app中填上要使用的```config```類型，即可套用到相應的設定

config 類型有以下幾種，詳細可以看```config.py``` 
```python
#config.py
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```




### 新增API

這邊建立一個測試API，單純回傳一個msg，
```python
@testapi.route('/testapi',methods=['GET'])
def testapi_m():
    try:
        return jsonify({"msg":"testapi OK"})
    except Exception as e:
        current_app.logger.warning(e,exc_info=True)
        return jsonify({"msg":"testapi fail"})
```

因為有使用Blueprint,所以記得在```app.__init__.py```設定
```python
#app.__init__.py
# import module
from app.api.testapi import testapi
# register blueprint
app.register_blueprint(testapi)
```


### 建立 Celery Worker 

```python
#celeryworker.py
from app import create_app,celery

app = create_app('default')
app.app_context().push()
```

celeryworker.py有兩個步驟要實現:
1. 建立一個Flask instance
2. 使用Flask application context，celery的動作都會在這邊進行


### 建立一個task

在```tasks```裡面是建立一個```add.py```，工作就是把接到的值相加後回傳
```python
#tasks.add.py
from app import celery

@celery.task(name='add')
def add(x, y):
    print('Hello job add')
    result = x + y
    return result
```


### 建立 celery config


這是celery的設定檔，跟原本的```config.py```分開比較好做後續的維護
```python
#celeryconfig.py
# import tasks
imports = (
    'tasks.add',
    'tasks.periodic'
    )

# #Timezone
enable_utc=False
timezone='Asia/Taipei'

# Broker and Backend
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# schedules : 設定tasks要多久啟動一次
from datetime import timedelta
from celery.schedules import crontab

beat_schedule = {
    'printy-run every 10 seconds': {
        'task': 'printy',
        'schedule': timedelta(seconds=10), #每10秒執行一次
        'args': (8,2)
    }
}
```

讀取這設定檔的地方在```app.__init__.py```

```python
#app.__init__.py
celery = Celery(__name__)
celery.config_from_object('tasks.celeryconfig')
```

### RUN


接著啟動服務

1. 打開一個新的terminal , run Flask app

```bash
$ python main.py
```

2. 打開一個新的terminal ,run celery worker

- windows
```bash
$ celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

- Linux
```bash
$ celery -A celery_worker.celery worker --loglevel=info
```

> 備註
```bash
$ celery -A [celery worker的檔案名稱].[celery名稱] worker --loglevel=info
```

- celery worker的檔案名稱 : 這邊使用```celeryworker.py```，所以是celeryworker
- celery 名稱 : 這個定義在```app.__init__.py```裡面的```celery = Celery(__name__)```


Request Test
---

測試時可以用瀏覽器或是postman去呼叫API，因為都是 ```GET``` methods

- 測試```testapi```


```http://127.0.0.1:5001/testapi```

可以得到
```
{
  "msg": "testapi OK"
}
```

- 測試```test add```

```http://127.0.0.1:5001/test_add```
```
{
  "RESULT": 35
}
```



定時任務
---

在```tasks```資料夾中建立```periodic.py```文件，加上定時任務的設定
```python
#tasks.periodic.py
from app import celery
@celery.task(name='printy')
def printy(a, b):
    """添加定時任務"""
    print('job printy')
    print(a + b)
    return a + b

```

在```tasks.celeryconfig.py```可以設定定時任務的名稱，只要使用此名稱，就可以使用這邊設定好的schedule
```python
beat_schedule = {
    'printy-run every 10 seconds': {
        'task': 'printy',
        'schedule': timedelta(seconds=10), #每10秒執行一次
        'args': (8,2)
    }
}
```


加上定時任務後，再次測試
---

> 如果flask和celery worker的terminal視窗還開著，可以直接執行下列動作

- 打開新的terminal,run celery beat
```bash
$ celery -A celery_worker.celery beat -l info -s log/celerybeat-schedule
```
- 說明
  - -l info : ```--loglevel=info```
  - -s log/celerybeat-schedule : 如果有log資料夾，celery會把產生的檔案放進去。如果沒有指定資料夾，則會在terminal目前所在的目錄下產生檔案


> 如果terminal關掉了，可以參考上方的[RUN](#run)步驟，再來執行此處的步驟。

到目前為止總共需要同時執行三個terminal
- Flask
- Celery worker
- Celery beat



Flower 監控
---
如果把程式放在production環境上，不可能時時刻刻進去裡面看任務狀態。因此會使用一套監控工具**flower**

- 開啟新的terminal
```bash
$ flower -A celery_worker.celery --port=5555
```

打開瀏覽器
```
http://localhost:5555/
```

選擇Processed分頁，可以看到頁面一直在更新，不斷的接收任務的進度和結果


到目前為止總共需要同時執行三個terminal
- Flask
- Celery worker
- Celery beat
- Flower

END
---
到這邊大致上flask+celery+flower就deploy完成了，但是在測試階段就需要開到四個terminal，如果到linux上面就會需要binding四個service。

因此這邊推薦使用```supervisor```來管理服務，一來方便測試，二來有GUI可以使用。


