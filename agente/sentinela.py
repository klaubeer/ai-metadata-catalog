"""
Integração com Sentinela AI — envia traces para avaliação e observabilidade.

Fire-and-forget via thread daemon. Nunca lança exceções.
"""

import logging
import os
import threading
import uuid
from datetime import datetime
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("data_navigator.sentinela")

SENTINELA_URL = os.getenv("SENTINELA_URL", "http://localhost:8000")
SENTINELA_API_KEY = os.getenv("SENTINELA_API_KEY", "sentinela-dev")

_habilitado = bool(SENTINELA_URL and SENTINELA_API_KEY)


def enviar_trace(
    nome: str,
    input: Any,
    output: Any,
    modelo: Optional[str] = None,
    latencia_ms: Optional[float] = None,
    metadata: Optional[dict] = None,
) -> None:
    """
    Envia um trace ao Sentinela em background (fire-and-forget).

    Args:
        nome: Nome da operação (ex: "data-navigator-chat")
        input: Pergunta do usuário
        output: Resposta do agente
        modelo: Modelo LLM utilizado
        latencia_ms: Latência total em milissegundos
        metadata: Metadados adicionais
    """
    if not _habilitado:
        return

    payload = {
        "id": str(uuid.uuid4()),
        "projeto": "data-navigator",
        "nome": nome,
        "input": input if isinstance(input, str) else str(input),
        "output": output if isinstance(output, str) else str(output),
        "modelo": modelo,
        "latencia_ms": latencia_ms,
        "metadata": metadata or {},
        "criado_em": datetime.utcnow().isoformat(),
    }

    def _enviar() -> None:
        try:
            with httpx.Client(timeout=5.0) as client:
                r = client.post(
                    f"{SENTINELA_URL}/traces",
                    json=payload,
                    headers={
                        "X-Api-Key": SENTINELA_API_KEY,
                        "Content-Type": "application/json",
                    },
                )
                r.raise_for_status()
                logger.debug("Sentinela: trace %s enviado", payload["id"])
        except Exception as exc:
            logger.debug("Sentinela: falha ao enviar trace — %s", exc)

    threading.Thread(target=_enviar, daemon=True).start()
