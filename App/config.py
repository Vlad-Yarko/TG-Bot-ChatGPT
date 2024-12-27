from dotenv import load_dotenv, find_dotenv
import os
from g4f.client import AsyncClient

load_dotenv(find_dotenv())

TOKEN=os.getenv('TOKEN')
DB=os.getenv('DB')

creator = '@TIGeR9999999999999'


from g4f.client import AsyncClient
from g4f.Provider import OpenaiChat

# client = AsyncClient(
#     provider=OpenaiChat,
#     image_provider=Gemini,
#     # Add other parameters as needed
# )

# client = AsyncClient(image_provider=OpenaiChat)
client = AsyncClient()
gpt_model = 'gpt-4'
gpt_model_image = 'flux'