# 代码生成时间: 2025-10-17 21:50:49
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServiceUnavailable, abort
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.log import logger
from sanic.config import Config
from sanic.blueprints import Blueprint
import json

# Initialize Sanic app
app = Sanic("LeaderboardService")

# In-memory leaderboard storage
leaderboard = []

# Leaderboard blueprint
bp = Blueprint('leaderboard', url_prefix='/leaderboard')

# Add a new score to the leaderboard
@bp.post("/add")
async def add_score(request: Request):
    try:
        # Parse JSON data from request
        data = request.json
        score = data.get("score\)
        name = data.get(