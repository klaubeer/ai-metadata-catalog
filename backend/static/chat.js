// função chamada pelos cards de sugestão

window.sugerir = function(texto){

const input = document.getElementById("pergunta")

input.value = texto
input.focus()

enviarPergunta()

}


// envio da pergunta

window.enviarPergunta = async function(){

const input = document.getElementById("pergunta")
const pergunta = input.value.trim()

if(!pergunta) return

const chat = document.getElementById("chat-box")

// mensagem do usuário

chat.innerHTML += `
<div class="msg user">
<div class="bubble">${pergunta}</div>
</div>
`

chat.scrollTop = chat.scrollHeight
input.value = ""

try{

const res = await fetch("/api/chat-api/",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
pergunta:pergunta
})
})

const data = await res.json()

// resposta do agente

chat.innerHTML += `
<div class="msg bot">
<div class="bubble">
${marked.parse(data.resposta || data.erro || "Sem resposta")}
</div>
</div>
`

chat.scrollTop = chat.scrollHeight

}catch(err){

console.error(err)

chat.innerHTML += `
<div class="msg bot">
<div class="bubble">
Erro ao conectar com o agente.
</div>
</div>
`

}

}