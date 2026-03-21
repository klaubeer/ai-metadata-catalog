import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from agente.agente import get_agente


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
        resposta = agente.invoke({"input": pergunta})

        return JsonResponse({"resposta": resposta["output"]})

    except Exception as e:

        return JsonResponse({"erro": str(e)}, status=500)
    
    