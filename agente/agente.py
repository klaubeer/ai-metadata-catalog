from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain.memory import ConversationBufferWindowMemory

from agente.ferramentas import search_tables, get_schema, quality_report
from agente.prompt import SYSTEM_PROMPT

# Instância única reutilizada entre requisições,
# preservando o histórico da conversa.
_agente_instance = None


def get_agente():
    global _agente_instance

    if _agente_instance is None:
        _agente_instance = _criar_agente()

    return _agente_instance


def _criar_agente():

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

        StructuredTool.from_function(
            func=search_tables,
            name="search_tables",
            description="Buscar tabelas relacionadas a um tema.",
        ),

        StructuredTool.from_function(
            func=get_schema,
            name="get_schema",
            description="Retorna as colunas de uma tabela pelo nome.",
        ),

        StructuredTool.from_function(
            func=quality_report,
            name="quality_report",
            description="Retorna métricas de qualidade de uma tabela pelo nome.",
        ),

    ]

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True
    )
