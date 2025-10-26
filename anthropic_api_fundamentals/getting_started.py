import os

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
my_api_key = os.getenv("ANTHROPIC_API_KEY")

# Create Anthropic client
client = Anthropic(api_key=my_api_key)

# Make a request to Claude asking for a joke
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=8000,
    messages=[
        {
            "role": "user",
            "content": "What should I search for to find the latest developments in C++?",
        }
    ],
)

# Print the response
# Access the text content from the response
content_block = response.content[0]
if isinstance(content_block, TextBlock):
    print(content_block.text)
