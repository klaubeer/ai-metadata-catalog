from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferWindowMemory

from agente.ferramentas import search_tables, get_schema, quality_report
from agente.prompt import SYSTEM_PROMPT


def criar_agente():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=10,
        return_messages=True
    )

    tools = [

        Tool(
            name="search_tables",
            func=search_tables,
            description="Buscar tabelas relacionadas a um tema."
        ),

        Tool(
            name="get_schema",
            func=get_schema,
            description="Retorna as colunas de uma tabela."
        ),

        Tool(
            name="quality_report",
            func=quality_report,
            description="Retorna métricas de qualidade de uma tabela."
        )

    ]

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True
    )

    return agent_executor
