# 代码生成时间: 2025-10-26 19:11:44
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse

# Define a class to generate breadcrumb trails
class BreadcrumbsService:
    def __init__(self, app: Sanic):
        """ Initialize the service and attach it to the application. """
        self.app = app
        self.breadcrumbs = {}  # Stores the breadcrumb trails

    async def add_breadcrumb(self, endpoint: str, breadcrumb: dict):
        """ Add a breadcrumb to the specified endpoint. """
        if endpoint not in self.breadcrumbs:
            self.breadcrumbs[endpoint] = []
        self.breadcrumbs[endpoint].append(breadcrumb)

    async def get_breadcrumbs(self, endpoint: str):
        """ Retrieve the breadcrumb trail for a given endpoint. """
        try:
            return self.breadcrumbs[endpoint]
        except KeyError:
            return []  # Return an empty list if no breadcrumbs are found

# Define the Sanic application
app = Sanic("BreadcrumbsApp")

# Initialize the BreadcrumbsService with the Sanic app
breadcrumbs_service = BreadcrumbsService(app)

# Define a route to add a breadcrumb
@app.route("/add_breadcrumb", methods=["POST"])
async def add_breadcrumb(request: Request):
    endpoint = request.json.get("endpoint")
    breadcrumb = request.json.get("breadcrumb")
    if not endpoint or not breadcrumb:
        return response.json({"error": "Missing endpoint or breadcrumb in request"}, status=400)
    await breadcrumbs_service.add_breadcrumb(endpoint, breadcrumb)
    return response.json({"message": "Breadcrumb added"}, status=200)

# Define a route to get breadcrumbs for an endpoint
@app.route("/get_breadcrumbs", methods=["GET"])
async def get_breadcrumbs(request: Request):
    endpoint = request.args.get("endpoint")
    if not endpoint:
        return response.json({"error": "Missing endpoint parameter"}, status=400)
    breadcrumbs = await breadcrumbs_service.get_breadcrumbs(endpoint)
    return response.json({"endpoint": endpoint, "breadcrumbs": breadcrumbs})

# Error handler for 404 Not Found
@app.exception_handler(404)
async def not_found(request: Request, exception: Exception):
    return response.json({"error": "Resource not found"}, status=404)

# Error handler for 500 Internal Server Error
@app.exception_handler(500)
async def server_error(request: Request, exception: Exception):
    return response.json({"error": "Internal server error"}, status=500)

if __name__ == '__main__':
    asyncio.run(app.create_server(start=True))