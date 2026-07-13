import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from tools import tool1, tool2, tool3

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
models = "gemini-3.1-flash-lite"
llm = ChatGoogleGenerativeAI(model=models, api_key=GEMINI_API_KEY)

tools = [tool1, tool2, tool3]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant that can use relevant tools to answer questions.",
)


def _message_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts).strip() or str(content)
    return str(content)


def main():
    print("AI Agent ready. Type 'quit' or 'exit' to stop.\n")
    messages = []

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        messages.append(HumanMessage(content=user_input))
        response = agent.invoke({"messages": messages})
        messages = response["messages"]
        print(f"Agent: {_message_text(messages[-1].content)}\n")


if __name__ == "__main__":
    main()
