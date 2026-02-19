import json
import httpx
from openai import OpenAI

from app.config import settings

LM_STUDIO_URL = "http://localhost:1234/v1"
API_URL = "http://localhost:8000"

client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_crm_data",
            "description": "Query customer data from the CRM system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filterParameter": {
                        "type": "string",
                        "enum": ["customer_id", "name", "email", "created_at", "status"],
                        "description": "The field to filter by."
                    },
                    "filterValue": {
                        "type": "string",
                        "description": "The value to match against the filter parameter."
                    },
                    "returnCount": {
                        "type": "integer",
                        "description": "Max number of results to return.",
                        "default": 3
                    },
                    "sortAscending": {
                        "type": "boolean",
                        "description": "True for ascending sort, False for descending."
                    }
                },
                "required": ["filterParameter", "filterValue"]
            }
        }
    },
]


def main():
    query = "Find active customers, sorted by name. use the `get_crm_data` tool"
    print(f"User Query: {query}")

    try:
        response = client.chat.completions.create(
            model="lfm2-700m-mlx",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant. Use the available tools to answer queries."},
                {"role": "user", "content": query}
            ],
            tools=tools,
            tool_choice="auto"
        )
    except Exception as e:
        print(f"Error calling LLM: {e}")
        print("Ensure LM Studio is running on port 1234 with the Local Server started.")
        return

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            print(f"\n[LLM Decision] Calling tool: {tool_call.function.name}")
            print(f"  Arguments: {tool_call.function.arguments}")

            if tool_call.function.name == "get_crm_data":
                args = json.loads(tool_call.function.arguments)
                try:
                    api_response = httpx.request(
                        "GET",
                        f"{API_URL}/data/crm",
                        headers={"x-api-key": settings.API_KEY[0]},
                        json=args
                    )
                    print(f"\n[API Response] Status: {api_response.status_code}")
                    print(f"  Data: {api_response.json()}")

                except Exception as api_err:
                    print(f"API Call Failed: {api_err}")

    else:
        print("\n[LLM Response] (No tool called)")
        print(message.content)


if __name__ == "__main__":
    main()
