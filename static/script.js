async function sendMessage() {
    const input = document.getElementById("user-input").value;
    if (!input) {
        alert("Please enter a message before sending.");
        return;
    }

    displayMessage("User", input);
    document.getElementById("user-input").value = "";  // Clear the input

    try {
        const response = await fetch("http://localhost:8000/submit_chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                text_input: input
            })
        });

        const data = await response.json();
        displayMessage("Bot", data.response);
    } catch (error) {
        console.error("Error sending message:", error);
        displayMessage("Bot", "Sorry, I couldn't process your request.");
    }
}

async function uploadImage() {
    const imageInput = document.getElementById("image-input");
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image before uploading.");
        return;
    }

    displayMessage("User", "Uploading image...");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/process_image", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        displayMessage("Bot", data.response);
    } catch (error) {
        console.error("Error uploading image:", error);
        displayMessage("Bot", "Sorry, I couldn't process the image.");
    }
}

async function clearChat() {
    try {
        const response = await fetch("http://localhost:8000/clear_chat", {
            method: "POST"
        });

        const data = await response.json();
        displayMessage("Bot", data.response);
    } catch (error) {
        console.error("Error clearing chat:", error);
        displayMessage("Bot", "Sorry, I couldn't clear the chat.");
    }
}

function displayMessage(sender, message) {
    const chatWindow = document.getElementById("chat-window");
    const messageElement = document.createElement("div");
    messageElement.className = sender === "User" ? "user-message" : "bot-message";
    messageElement.textContent = `${sender}: ${message}`;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

document.getElementById("chat-form").addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage();
});
