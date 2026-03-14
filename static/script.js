const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message");

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const message = input.value;

    // show user message
    const userMsg = document.createElement("div");
    userMsg.className = "user";
    userMsg.innerText = "You: " + message;
    chatBox.appendChild(userMsg);

    // send message to Flask
    const response = await fetch("/",{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body:"message=" + encodeURIComponent(message)
    });

    const html = await response.text();

    // parse returned HTML
    const parser = new DOMParser();
    const doc = parser.parseFromString(html,"text/html");

    const botReply = doc.querySelector("p b") ?
        doc.querySelector("p").innerText :
        "";

    const botMsg = document.createElement("div");
    botMsg.className="bot";
    botMsg.innerText = "Bot: " + botReply;

    chatBox.appendChild(botMsg);

    input.value="";

    chatBox.scrollTop = chatBox.scrollHeight;

});