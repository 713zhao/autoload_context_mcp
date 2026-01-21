from openai import OpenAI
from agent.context_router import build_system_context

client = OpenAI()

def ask_agent(prompt, model="gpt-4o-mini"):
    system = build_system_context(prompt)
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content
