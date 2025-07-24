"""Simple AWS chatbot using LangChain tools."""

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from . import aws_tools


def create_agent() -> "AgentExecutor":
    llm = ChatOpenAI(temperature=0)
    tools = [
        aws_tools.count_public_s3_buckets,
        aws_tools.describe_bucket_contents,
        aws_tools.ec2_instance_type_by_ip,
        aws_tools.describe_user_permissions,
    ]
    return initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)


def main() -> None:
    agent = create_agent()
    print("AWS Chatbot. Type 'quit' to exit.")
    while True:
        try:
            query = input("> ")
        except EOFError:
            break
        if not query or query.lower() in {"quit", "exit"}:
            break
        result = agent.run(query)
        print(result)


if __name__ == "__main__":
    main()
