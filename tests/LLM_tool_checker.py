import json
import httpx
from openai import OpenAI

LM_STUDIO_URL = "http://localhost:1234/v1"
API_URL = "http://localhost:8000"

client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")

# 2. Define the Tool Schema
#    (In a real app, you might generate this from app.openapi())
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
    # You can add get_support_data and get_analytics_data here similarly
]


def main():
    query = "Find the recently joined customers in the last month upto today, the current date is 2026-01-11 and the date timestamp is of the form 2026-01-11T03:46:48.375809"
    # query = "Find active customers, sorted by name."
    print(f"User Query: {query}")

    # 3. Call the LLM with Tools
    try:
        response = client.chat.completions.create(
            model="lfm2-700m-mlx",  # LM Studio usually ignores this or uses loaded model
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

    # 4. Handle Tool Calls
    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            print(f"\n[LLM Decision] Calling tool: {tool_call.function.name}")
            print(f"  Arguments: {tool_call.function.arguments}")

            # 5. Execute Code (Simulated here, but you would call your API)
            if tool_call.function.name == "get_crm_data":
                args = json.loads(tool_call.function.arguments)
                try:
                    # Map filterValue to int if param is ID, else keep str?
                    # Your API handles string inputs mostly or requires strict types.
                    # Let's just pass what the API expects.

                    # NOTE: Your API expects POST or GET? Router uses GET with JSON body (unusual) or Query params?
                    # Your router uses: get_data_crm(payload: SourcePayloadCRM)
                    # FastAPI with Pydantic model in GET request usually expects QUERY params if not Body.
                    # But SourcePayloadCRM is a complex model. FastAPI default is "Body" for Pydantic models in GET unless Depends() is used.
                    # Most clients/browsers strip Body from GET. Creating valid request:

                    # Let's try sending as JSON body (httpx supports it)
                    api_response = httpx.request(
                        "GET",
                        f"{API_URL}/data/crm",
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
