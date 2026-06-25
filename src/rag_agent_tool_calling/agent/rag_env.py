from dotenv import load_dotenv
load_dotenv()
import os

def load_rag_env() -> None:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError('Err:missing openai api key')
    os.environ['OPENAI_API_KEY'] = openai_api_key
    print('openai api key set', openai_api_key[0:15])

    langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
    if not langsmith_api_key:
        raise ValueError('Err:missing langsmith api key')
    os.environ['LANGSMITH_API_KEY'] = langsmith_api_key
    print('langsmith api key set', langsmith_api_key[0:15])
