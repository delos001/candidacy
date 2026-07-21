## Title: Smoke Test for Claude API
## Author: Jason Delosh
## Date: 2026-07-10

"""
This test script is to verify Claude API call succeeds:
- verify API key (secret in .env file   )
- funding billing balance
- environment loading
"""

## load required libraries
## - dotenv is library to read/load .env files (using load_dotenv): it is a courier in
##   the sense that it delivers secrets from a .env file to the variable then steps away
## - ChatAnthropic is the langchain wrapper for Anthropic Claude API
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv("spike/.env")  # .env = plain english file with secrets: Anthoropic API key

## assign a variable to the model you want and set token maximums.
## Claude has a max token limit of 100k tokens, but you can set your own limit lower.
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=50)

## invoke sends one prompt and blocks until the llm answers.
## .content is the text of that answer
print(llm.invoke("Say hell in exactly five words.").content)
