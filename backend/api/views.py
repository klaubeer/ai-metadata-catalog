import json
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from agente.agente import get_agente
from agente.sentinela import enviar_trace as sentinela_trace


def home(request):
    return render(request, "home.html")


def chat_page(request):
    return render(request, "chat/chat.html")


@csrf_exempt
def chat(request):

    if request.method != "POST":
        return JsonResponse({"erro": "Metodo invalido"}, status=400)

    try:

        body = json.loads(request.body.decode("utf-8"))
        pergunta = body.get("pergunta")

        if not pergunta:
            return JsonResponse({"erro": "Pergunta nao enviada"}, status=400)

        agente = get_agente()

        inicio = time.time()
        resposta = agente.invoke({"input": pergunta})
        latencia_ms = (time.time() - inicio) * 1000

        texto_resposta = resposta["output"]

        # Envia trace ao Sentinela (fire-and-forget)
        sentinela_trace(
            nome="data-navigator-chat",
            input=pergunta,
            output=texto_resposta,
            modelo="gpt-4o-mini",
            latencia_ms=round(latencia_ms, 2),
        )

        return JsonResponse({"resposta": texto_resposta})

    except Exception as e:

        return JsonResponse({"erro": str(e)}, status=500)
    
    