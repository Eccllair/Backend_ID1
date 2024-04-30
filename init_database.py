import asyncio
from database import init_models, init_test_models

asyncio.run(init_models())
asyncio.run(init_test_models())