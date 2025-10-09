# 代码生成时间: 2025-10-10 03:06:19
import sanic
from sanic.response import json
import random
import asyncio

# Define the app
app = sanic.Sanic("RandomNumberGenerator")

# Define the route for generating a random number
@app.route("/random", methods=["GET"])
async def generate_random_number(request):
    # Get the bounds from the query parameters
    try:
        lower_bound = int(request.args.get("lower", 1))
        upper_bound = int(request.args.get("upper", 100))
    except ValueError:
        return json({"error": "Invalid range. Please provide integers."}, status=400)

    # Ensure the range is valid
    if lower_bound >= upper_bound:
        return json({"error": "Invalid range. Lower bound must be less than upper bound."}, status=400)

    # Generate a random number within the specified range
    random_number = random.randint(lower_bound, upper_bound)
    return json({"random_number": random_number})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=1)