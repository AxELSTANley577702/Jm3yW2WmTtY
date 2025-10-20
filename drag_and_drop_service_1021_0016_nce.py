# 代码生成时间: 2025-10-21 00:16:51
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, BadRequest
from sanic.response import html, json as sanic_json
from sanic.views import HTTPMethodView
from jinja2 import Environment, FileSystemLoader

# Initialize the Sanic application
app = Sanic("DragAndDropService")

# Load templates from a local directory
env = Environment(loader=FileSystemLoader("./templates"))

# Define the DragAndDropView to handle requests
class DragAndDropView(HTTPMethodView):
    async def get(self, request):
        # Render the drag and drop interface template
        template = env.get_template("drag_and_drop.html")
        return response.html(template.render())

    async def post(self, request):
        # Validate and parse the incoming JSON data
        try:
            order = request.json
            # Perform error handling and validation
            if not order or not isinstance(order, list):
                return sanic_json({'error': 'Invalid order data'}, status=400)
            # Assuming that the order data is a list of integers representing the new order
            # Save the order to a database or perform the necessary operations
            # For this example, we are just returning the saved order
            return sanic_json({'new_order': order})
        except json.JSONDecodeError:
            return sanic_json({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            raise ServerError("An error occurred while processing the request", e)

# Add the route for the drag and drop interface
app.add_route(DragAndDropView.as_view(), "/drag_and_drop")

# Define the main function to run the application
def main():
    app.run(host="0.0.0.0", port=8000, debug=True)

# Run the application if it's the main module
if __name__ == "__main__":
    main()

# Below is the HTML template for the drag and drop interface
# It should be placed in the ./templates/drag_and_drop.html file
# <!DOCTYPE html>
# <html lang="en">\# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Drag and Drop Interface</title>
#     <!-- Drag and drop script and style links here -->
# </head>
# <body>
#     <div id="drag-and-drop-container">
#         <!-- Items that can be dragged and sorted will be listed here -->
#     </div>
#     <script>
#         // Script to handle drag and drop functionality
#         // This script will interact with the backend to update the order
#     </script>
# </body>
# </html>