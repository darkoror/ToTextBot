from environs import Env

env = Env()
env.read_env()

TEST_TOKEN = env('TEST_TOKEN')
TOKEN = env('TOKEN')

# Wit.ai
EN_SERVER_ACCESS_TOKEN = env('EN_SERVER_ACCESS_TOKEN')
WIT_AI_API_ENDPOINT = env('WIT_AI_API_ENDPOINT')

# CREDENTIALS = env.dict('CREDENTIALS', subcast_keys=str, subcast_values=str)
