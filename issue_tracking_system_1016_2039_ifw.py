# 代码生成时间: 2025-10-16 20:39:44
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, abort
import uuid


# 定义缺陷跟踪系统应用
app = Sanic("IssueTrackingSystem")

# 存储缺陷的内存数据库
issues = []


# 定义缺陷数据模型
class Issue:
    def __init__(self, title, description, assignee):
        self.id = str(uuid.uuid4())  # 使用UUID生成唯一的ID
        self.title = title
        self.description = description
        self.assignee = assignee
        self.status = "Open"  # 初始状态为Open

    # 将缺陷转换为字典
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "status": self.status
        }


# 添加缺陷的路由
@app.route("/issues", methods=["POST"])
async def add_issue(request: Request):
    # 从请求体中获取数据
    data = request.json
    
    # 验证数据
    if not all(key in data for key in ("title", "description", "assignee")):
        abort(400, "Missing required fields")
    
    # 创建新的缺陷
    issue = Issue(data["title"], data["description"], data["assignee"])
    issues.append(issue)
    
    # 返回新创建的缺陷
    return response.json(issue.to_dict(), status=201)

# 获取所有缺陷的路由
@app.route("/issues", methods=["GET"])
async def get_issues(request: Request):
    # 返回所有缺陷
    return response.json([i.to_dict() for i in issues])

# 获取单个缺陷的路由
@app.route("/issues/<issue_id>", methods=["GET"])
async def get_issue(request: Request, issue_id: str):
    # 根据ID查找缺陷
    issue = next((i for i in issues if i.id == issue_id), None)
    if not issue:
        abort(404, "Issue not found")
    return response.json(issue.to_dict())

# 更新缺陷状态的路由
@app.route("/issues/<issue_id>/status", methods=["PUT"])
async def update_issue_status(request: Request, issue_id: str):
    # 从请求体中获取新状态
    new_status = request.json.get("status")
    
    # 根据ID查找缺陷
    issue = next((i for i in issues if i.id == issue_id), None)
    if not issue:
        abort(404, "Issue not found")
    
    # 更新缺陷状态
    issue.status = new_status
    return response.json(issue.to_dict())

# 删除缺陷的路由
@app.route("/issues/<issue_id>", methods=["DELETE"])
async def delete_issue(request: Request, issue_id: str):
    # 根据ID查找缺陷
    issue = next((i for i in issues if i.id == issue_id), None)
    if not issue:
        abort(404, "Issue not found")
    
    # 从列表中移除缺陷
    issues = [i for i in issues if i.id != issue_id]
    return response.json({"message": "Issue deleted"}, status=204)


# 运行应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)