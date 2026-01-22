import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from app.main import app

# Create ASGI adapter
adapter = Mangum(app, lifespan="off")

# Export as a function instead of a handler variable
def handler(event, context):
    return adapter(event, context)