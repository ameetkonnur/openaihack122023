from aisearchhelper import *
import os
import openai
import json

query = "tender topic, submission date, submission address & earnest money"

functions= [  
    {
        "name": "azure_ai_search",
        "description": "given a query uses azure ai search to search it's index and return the results",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Search Query parameters for the Azure AI Search Index. If multiple data points requested then list all of them comma separated."
                }
            },
            "required": ["search_query"]
        }
    }
]

def azure_ai_search(search_query):
    
    query = search_query.split(",")
    search_content = ""
    for q in query:
        # response = single_vector_search(q) # if search has to be done without filtering by owner
        response = single_vector_search_with_filter(q,"ameetk") # if search has to be filtered by owner
        if response:
            search_content = search_content + "\n" + response
    return search_content

system_message = """You are an assistant designed to help people understand tender documents specifics from a tender PDF file uploaded.
The user may ask for multiple data points in the tender document and you will identify each of the data points and try to answer all of them.
You have access to a PDF reader that can read the tender document and extract the relevant information.
Make sure the answer is detailed and relevant and is not a very brief summary.
"""
messages= [{"role": "system", "content": system_message},
    {"role": "user", "content": query},
]

openai.api_key=os.getenv("OPENAI_API_KEY")  
openai.api_version="2023-10-01-preview"
api_model=os.getenv("OPENAI_API_MODEL")
openai.api_type="azure"
openai.api_base = os.getenv("OPENAI_API_URL")

response = openai.chat.completions.create(
    model=api_model,
    messages= messages,
    functions = functions,
    function_call="auto",
)

output = response.choices[0].message
print(output)

if "function_call" in str(output):
    function_name = output.function_call.name
    function_arguments = json.loads(output.function_call.arguments)
    available_functions = {
            "azure_ai_search": azure_ai_search,
    }
    function_to_call = available_functions[function_name]
    print(function_arguments)
    function_response = function_to_call(**function_arguments)

    messages.append(
        {"role": output.role, 
         "function_call":{
             "name": str(function_name), 
             "arguments": str(function_arguments)}, 
             "content": None})
    messages.append({"role": "function", "name" : str(function_name), "content": str(function_response)})

    response = openai.chat.completions.create(
        model=api_model,
        messages= messages,
        functions = functions,
        function_call="auto",
    )
    output = response.choices[0].message
    print("\n" + output.content)
