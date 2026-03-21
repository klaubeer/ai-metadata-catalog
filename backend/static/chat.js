window.sugerir = function(texto) {
    const input = document.getElementById("pergunta")
    input.value = texto
    input.focus()
    enviarPergunta()
}


window.enviarPergunta = async function() {

    const input = document.getElementById("pergunta")
    const pergunta = input.value.trim()

    if (!pergunta) return

    const chat = document.getElementById("chat-box")

    // mensagem do usuário
    chat.innerHTML += `
        <div class="msg user">
            <div class="bubble">${pergunta}</div>
        </div>
    `

    input.value = ""
    input.disabled = true
    document.querySelector("#input-area button").disabled = true
    chat.scrollTop = chat.scrollHeight

    // loading
    const loadingId = "loading-" + Date.now()
    chat.innerHTML += `
        <div class="msg bot" id="${loadingId}">
            <div class="bubble loading">
                <span></span><span></span><span></span>
            </div>
        </div>
    `
    chat.scrollTop = chat.scrollHeight

    try {

        const res = await fetch("/api/chat-api/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pergunta })
        })

        const data = await res.json()

        document.getElementById(loadingId).remove()

        chat.innerHTML += `
            <div class="msg bot">
                <div class="bubble">
                    ${marked.parse(data.resposta || data.erro || "Sem resposta")}
                </div>
            </div>
        `

    } catch (err) {

        console.error(err)
        document.getElementById(loadingId).remove()

        chat.innerHTML += `
            <div class="msg bot">
                <div class="bubble">
                    Erro ao conectar com o agente.
                </div>
            </div>
        `

    } finally {

        input.disabled = false
        document.querySelector("#input-area button").disabled = false
        input.focus()
        chat.scrollTop = chat.scrollHeight

    }

}
