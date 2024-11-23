from flask import Flask, request, g
import uuid
from logger_config import configure_logger

app = Flask(__name__)

def setup_logger(request_id):
    logger = configure_logger(request_id=request_id)
    g.logger = logger
    return logger

@app.before_request
def before_request():
    """
    Runs before processing each request.
    Sets up a request-specific logger.
    """
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.request_id = request_id

    setup_logger(request_id)

@app.after_request
def after_request(response):
    """
    Runs after processing each request.
    Cleans up the logger to avoid redundant handlers.
    """
    if hasattr(g, "logger"):
        for handler in g.logger.handlers:
            handler.close()
            g.logger.removeHandler(handler)
    return response

@app.route("/")
def index():
    """
    Example route that uses the request-specific logger.
    """
    g.logger.info("Processing request in index route.")
    return "Hello, World!"

@app.route("/example")
def example():
    """
    Another route for testing logging.
    """
    g.logger.info("Processing request in example route.")
    return "This is an example route!"

if __name__ == "__main__":
    app.run(debug=True)
