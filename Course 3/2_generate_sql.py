"""
Step 4: Use Claude API with the schema context to generate SQL queries
that produce aggregated, meaningful indicators from the data.
"""
import json
import re
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from utils import format_schema_for_prompt

load_dotenv()


def generate_sql():
    with open("context.json", "r", encoding="utf-8") as f:
        context = json.load(f)

    schema_text = format_schema_for_prompt(context)

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=(
            "You are a SQL expert. Generate practical aggregated SQL queries "
            "based on the provided MySQL database schema."
        ),
        messages=[
            {
                "role": "user",
                "content": f"""Based on this MySQL database schema, generate 6-8 SQL queries
that provide useful aggregated insights and key metrics.

SCHEMA:
{schema_text}

Requirements for each query:
- Use aggregation: COUNT, SUM, AVG, MIN, MAX, GROUP BY, ORDER BY
- Be practically useful for understanding patterns in the data
- Add a short comment explaining what it measures

Return ONLY valid JSON in this exact format:
{{
  "queries": [
    {{"description": "...", "sql": "SELECT ..."}},
    ...
  ]
}}""",
            }
        ],
    )

    content = response.content[0].text

    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        queries_data = json.loads(json_match.group())
    else:
        queries_data = {"raw_response": content}

    with open("generated_queries.json", "w", encoding="utf-8") as f:
        json.dump(queries_data, f, indent=2, ensure_ascii=False)

    if "queries" in queries_data:
        print(f"Generated {len(queries_data['queries'])} SQL queries:")
        for i, q in enumerate(queries_data["queries"], 1):
            print(f"\n  {i}. {q['description']}")
            print(f"     {q['sql'][:120]}...")
    else:
        print("Raw response saved to generated_queries.json")

    return queries_data


if __name__ == "__main__":
    generate_sql()
