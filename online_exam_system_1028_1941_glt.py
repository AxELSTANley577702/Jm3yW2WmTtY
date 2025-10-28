# 代码生成时间: 2025-10-28 19:41:31
import sanic
from sanic.response import json, html
from jinja2 import Environment, FileSystemLoader
import os

# 设置模板文件夹路径
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# 数据存储
questions = [
    {
        "id": 1,
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    # 更多问题...
]

app = sanic.Sanic('OnlineExamSystem')

@app.route('/')
async def test(request):
    """
    返回考试系统的首页，用户可以查看问题并提交答案
    """
    return html(env.get_template('index.html').render(questions=questions))

@app.route('/submit', methods=['POST'])
async def submit(request):
    """
    处理用户提交的答案
    """
    try:
        answers = request.json.get('answers')
        # 这里可以添加更多的逻辑来验证答案是否正确
        correct_answers = sum(1 for q, a in zip(questions, answers) if q['answer'] == a)
        return json({'correct_answers': correct_answers, 'total_questions': len(questions)})
    except Exception as e:
        # 错误处理
        return json({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
