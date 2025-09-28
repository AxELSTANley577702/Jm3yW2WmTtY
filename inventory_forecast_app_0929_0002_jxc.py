# 代码生成时间: 2025-09-29 00:02:58
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound, abort
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
import os

# 定义应用
app = sanic.Sanic('inventory_forecast_app')

# 模型加载函数
def load_model():
    if os.path.exists('inventory_model.pkl'):
        with open('inventory_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    else:
        raise FileNotFoundError('Inventory model file not found')

# 预测库存函数
def predict_inventory(history):
    if isinstance(history, list) and len(history) > 0:
        try:
            model = load_model()
            history = np.array(history).reshape(-1, 1)
            return model.predict(history)[0]
        except Exception as e:
            raise ServerError(f'Error in inventory prediction: {str(e)}')
    else:
        raise ValueError('Invalid history data')

# 库存预测API
@app.route('/predict', methods=['POST'])
async def predict(request):
    try:
        data = request.json
        history = data.get('history')
        prediction = predict_inventory(history)
        return json({'prediction': prediction}, status=200)
    except ValueError as e:
        return json({'error': str(e)}, status=400)
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 健康检查API
@app.route('/ping', methods=['GET'])
async def ping(request):
    return json({'status': 'ok'}, status=200)

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)