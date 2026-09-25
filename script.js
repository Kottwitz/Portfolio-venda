const API_URL = "https://portfolio-venda.onrender.com/chat";
let chatHistory = [];

// Controlo do Menu Mobile Hambúrguer
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    const hamburgerIcon = document.querySelector('#menuHamburger i');
    
    navLinks.classList.toggle('active');
    
    if (navLinks.classList.contains('active')) {
        hamburgerIcon.classList.remove('fa-bars');
        hamburgerIcon.classList.add('fa-times');
    } else {
        hamburgerIcon.classList.remove('fa-times');
        hamburgerIcon.classList.add('fa-bars');
    }
}

function closeMenu() {
    const navLinks = document.getElementById('navLinks');
    const hamburgerIcon = document.querySelector('#menuHamburger i');
    
    navLinks.classList.remove('active');
    hamburgerIcon.classList.remove('fa-times');
    hamburgerIcon.classList.add('fa-bars');
}

// Controlo do Chat Widget
function toggleChat() {
    const chatBox = document.getElementById('chatBox');
    chatBox.classList.toggle('active');
}

function sendQuickMessage(text) {
    document.getElementById('userInput').value = text;
    handleSendMessage(new Event('submit'));
}

async function handleSendMessage(e) {
    e.preventDefault();
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    const botMessageDiv = appendMessage('bot', '...');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pergunta: message,
                historico: chatHistory
            })
        });

        if (!response.ok) throw new Error("Erro na comunicação com a API");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        botMessageDiv.textContent = '';

        let fullText = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            fullText += chunk;
            botMessageDiv.textContent = fullText;
            scrollToBottom();
        }

        chatHistory.push({ role: 'user', content: message });
        chatHistory.push({ role: 'assistant', content: fullText });

    } catch (error) {
        botMessageDiv.textContent = "⚠️ Erro ao conectar ao servidor. Fale no WhatsApp: (47) 98825-8610.";
    }
}

function appendMessage(sender, text) {
    const messagesDiv = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    msgDiv.textContent = text;
    messagesDiv.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv;
}

function scrollToBottom() {
    const messagesDiv = document.getElementById('chatMessages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}