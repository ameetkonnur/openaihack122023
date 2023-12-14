import os
import openai
import requests
import json

openai.api_key=os.getenv("OPENAI_API_KEY")  
openai.api_version="2023-10-01-preview"
api_model=os.getenv("OPENAI_API_MODEL")
openai.api_type="azure"
openai.api_base = os.getenv("OPENAI_API_URL")
bing_api_key = os.getenv("BING_API_KEY")

system_message = """You are an assistant designed to help people answer questions.
You have access to query the web using Bing Search. You should call bing search whenever a question requires up to date information or could benefit from web data.
"""
messages= [{"role": "system", "content": system_message},
    {"role": "user", "content": "who is CM of Rajasthan"},
]

functions= [  
    {
        "name": "bing_search",
        "description": "Retrieves data from the bing search index based on the question & teh recency of the data that is sought ",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Search Query"
                }
            },
            "required": ["search_query"]
        }
    }
]  

response = openai.ChatCompletion.create(
    engine=api_model,
    messages= messages,
    functions = functions,
    function_call="auto",
)

def bing_search(search_query):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    response = requests.get(url, headers=headers, params={"q": search_query,"freshness": "2023-05-01..2023-12-31"})
    response.raise_for_status()
    search_results = response.json()

    output = []

    for result in search_results['webPages']['value']:
        output.append({
            'title': result['name'],
            'link': result['url'],
            'snippet': result['snippet']
        })
    return json.dumps(output)

output = response.choices[0].message
print(output)

# check if output has key function_call or content, 
# if function_call then get the function name from the key name, else print the content value.
# get the parameters for the function from the arguments array 
# call the function with the parameters and the value given in arguments.
# return the output of the function to the openai chatbot.

if "function_call" in output:
    function_name = output["function_call"]["name"]
    function_arguments = json.loads(output["function_call"].arguments)
    print(function_name)
    available_functions = {
            "bing_search": bing_search,
    }
    function_to_call = available_functions[function_name]
    print(function_arguments)
    function_response = function_to_call(**function_arguments)
    print(function_response)
    messages.append(
        {"role": output["role"], 
         "function_call":{
             "name": output["function_call"].name, 
             "arguments": output["function_call"].arguments }, 
             "content": None})
    messages.append({"role": "function", "name" : function_name, "content": function_response})

    #for message in messages:
    #    print(message)
    #    print()
    
    response = openai.ChatCompletion.create(
        engine=api_model,
        messages= messages,
        functions = functions,
        function_call="auto",
    )
    output = response.choices[0].message
    print(output)