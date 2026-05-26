// Initialize Lucide Icons on load
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
    loadHistory();
});

// Store the current active chat ID
let currentChatId = null;
const BACKEND_URL = "http://127.0.0.1:8000";

// DOM Elements
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");
const historyList = document.getElementById("historyList");
const newChatBtn = document.getElementById("newChatBtn");
const emptyState = document.getElementById("emptyState");

// Modal Elements
const deleteModal = document.getElementById("deleteModal");
const deleteModalContent = document.getElementById("deleteModalContent");
const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
let chatToDeleteId = null;

const editModal = document.getElementById("editModal");
const editModalContent = document.getElementById("editModalContent");
const cancelEditBtn = document.getElementById("cancelEditBtn");
const confirmEditBtn = document.getElementById("confirmEditBtn");
const editTitleInput = document.getElementById("editTitleInput");
let chatToEditId = null;

// Handle form submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // Clear input
    userInput.value = "";
    
    // Add User Message to UI
    appendMessage(text, "user");

    // Add loading indicator
    const loadingId = addTypingIndicator();

    try {
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: text,
                chat_id: currentChatId // Will be null for new chats
            })
        });

        const data = await response.json();
        
        // Remove loading indicator
        removeElement(loadingId);

        if (response.ok) {
            // Update current chat ID if this was a new chat
            if (!currentChatId) {
                currentChatId = data.chat_id;
                loadHistory(); // Reload sidebar
            }
            appendMessage(data.answer, "ai");
        } else {
            appendMessage("An error occurred processing your request.", "ai");
        }

    } catch (error) {
        removeElement(loadingId);
        appendMessage("Network error. Is the backend running?", "ai");
    }
});

// Start new chat
newChatBtn.addEventListener("click", () => {
    currentChatId = null;
    chatBox.innerHTML = "";
    chatBox.appendChild(emptyState);
    emptyState.style.display = "flex";
    
    // Remove active styling from history items
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('bg-zinc-800', 'text-zinc-200');
        item.classList.add('text-zinc-400');
    });
});

// Fetch and render sidebar history
async function loadHistory() {
    try {
        const response = await fetch(`${BACKEND_URL}/history`);
        const chats = await response.json();
        
        historyList.innerHTML = "";
        
        chats.forEach(chat => {
            const isActive = chat.id === currentChatId;
            const btn = document.createElement("div");
            
            // Container for the history item
            btn.className = `history-item w-full p-2.5 rounded-lg transition-all duration-200 text-sm flex items-center justify-between group cursor-pointer ${
                isActive 
                ? 'bg-zinc-800 text-zinc-200' 
                : 'text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-300'
            }`;
            
            btn.innerHTML = `
                <div class="flex items-center gap-3 overflow-hidden flex-1" onclick="loadChatDetails('${chat.id}')">
                    <i data-lucide="message-square" class="w-4 h-4 shrink-0 opacity-70 group-hover:opacity-100 transition-opacity"></i>
                    <span class="font-medium truncate w-full">${escapeHTML(chat.title)}</span>
                </div>
                <div class="flex items-center shrink-0 opacity-0 group-hover:opacity-100 transition-all">
                    <button onclick="openEditModal('${chat.id}', '${escapeHTML(chat.title).replace(/'/g, "\\'")}')" class="p-1 rounded hover:bg-zinc-700 hover:text-blue-400 text-zinc-500 mr-1">
                        <i data-lucide="pencil" class="w-3.5 h-3.5"></i>
                    </button>
                    <button onclick="deleteChat('${chat.id}')" class="p-1 rounded hover:bg-zinc-700 hover:text-red-400 text-zinc-500">
                        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
            `;
            
            historyList.appendChild(btn);
        });

        // Re-initialize newly added icons
        lucide.createIcons();
    } catch (error) {
        console.error("Failed to load history", error);
    }
}

// Fetch and render a specific past chat
async function loadChatDetails(chatId) {
    try {
        const response = await fetch(`${BACKEND_URL}/history/${chatId}`);
        const chatData = await response.json();
        
        currentChatId = chatData.id;
        chatBox.innerHTML = "";
        
        chatData.qa_pairs.forEach(pair => {
            appendMessage(pair.question, "user");
            appendMessage(pair.answer, "ai");
        });

        loadHistory();
    } catch (error) {
        console.error("Failed to load chat details", error);
    }
}

// Function to trigger the custom delete modal
function deleteChat(chatId) {
    chatToDeleteId = chatId;
    // Show modal
    deleteModal.classList.remove("opacity-0", "pointer-events-none");
    deleteModalContent.classList.remove("scale-95");
    deleteModalContent.classList.add("scale-100");
}

// Function to hide the custom delete modal
function closeDeleteModal() {
    chatToDeleteId = null;
    // Hide modal
    deleteModal.classList.add("opacity-0", "pointer-events-none");
    deleteModalContent.classList.remove("scale-100");
    deleteModalContent.classList.add("scale-95");
}

// Cancel deletion
cancelDeleteBtn.addEventListener("click", closeDeleteModal);

// Confirm deletion
confirmDeleteBtn.addEventListener("click", async () => {
    if (!chatToDeleteId) return;
    const chatId = chatToDeleteId;
    closeDeleteModal(); // Close immediately for responsive UI

    try {
        const response = await fetch(`${BACKEND_URL}/history/${chatId}`, {
            method: "DELETE"
        });

        if (response.ok) {
            if (currentChatId === chatId) {
                newChatBtn.click();
            } else {
                loadHistory(); 
            }
            showToast("Chat deleted successfully");
        } else {
            console.error("Failed to delete chat.");
        }
    } catch (error) {
        console.error("Error deleting chat", error);
    }
});

// Edit Chat Title Logic
function openEditModal(chatId, currentTitle) {
    chatToEditId = chatId;
    editTitleInput.value = currentTitle;
    editModal.classList.remove("opacity-0", "pointer-events-none");
    editModalContent.classList.remove("scale-95");
    editModalContent.classList.add("scale-100");
    setTimeout(() => editTitleInput.focus(), 100);
}

function closeEditModal() {
    chatToEditId = null;
    editModal.classList.add("opacity-0", "pointer-events-none");
    editModalContent.classList.remove("scale-100");
    editModalContent.classList.add("scale-95");
}

cancelEditBtn.addEventListener("click", closeEditModal);

confirmEditBtn.addEventListener("click", async () => {
    if (!chatToEditId) return;
    const newTitle = editTitleInput.value.trim();
    if (!newTitle) return; // Don't allow empty titles

    const chatId = chatToEditId;
    closeEditModal();

    try {
        const response = await fetch(`${BACKEND_URL}/history/${chatId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: newTitle })
        });

        if (response.ok) {
            loadHistory(); // Reload sidebar to show new title
            showToast("Chat renamed successfully");
        } else {
            console.error("Failed to rename chat.");
        }
    } catch (error) {
        console.error("Error renaming chat", error);
    }
});

// Append a message to the UI
function appendMessage(text, sender) {
    if (emptyState && emptyState.style.display !== "none") {
        emptyState.style.display = "none";
    }

    const div = document.createElement("div");
    const isUser = sender === "user";
    
    div.className = `flex w-full ${isUser ? "justify-end" : "justify-start"} opacity-0 translate-y-2 animate-fade-in`;
    
    // Minimalist bubble styling
    const bubbleContent = isUser 
        ? `<div class="bg-zinc-800 text-zinc-200 px-5 py-3.5 rounded-2xl rounded-tr-sm max-w-[75%] text-[15px] leading-relaxed shadow-sm">
             ${escapeHTML(text)}
           </div>`
        : `<div class="flex gap-4 max-w-[85%]">
             <div class="w-8 h-8 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-center shrink-0 mt-1">
                 <i data-lucide="bot" class="w-4 h-4 text-zinc-400"></i>
             </div>
             <div class="text-zinc-300 py-1.5 text-[15px] leading-relaxed">
                 ${escapeHTML(text)}
             </div>
           </div>`;
           
    div.innerHTML = bubbleContent;
    chatBox.appendChild(div);
    
    // Render the bot icon if it's an AI message
    if (!isUser) lucide.createIcons();
    
    // Simple custom animation via CSS inline or rely on tailwind if defined, 
    // for simplicity, we trigger a reflow to fade it in
    requestAnimationFrame(() => {
        div.style.transition = "all 0.3s ease-out";
        div.style.opacity = "1";
        div.style.transform = "translateY(0)";
    });

    scrollToBottom();
}

// Typing indicator
function addTypingIndicator() {
    if (emptyState) emptyState.style.display = "none";
    
    const id = "typing-" + Date.now();
    const div = document.createElement("div");
    div.id = id;
    div.className = "flex w-full justify-start opacity-0 translate-y-2";
    div.innerHTML = `
        <div class="flex gap-4 max-w-[85%]">
             <div class="w-8 h-8 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-center shrink-0 mt-1">
                 <i data-lucide="bot" class="w-4 h-4 text-zinc-400"></i>
             </div>
             <div class="flex gap-1 items-center py-3">
                <div class="w-1.5 h-1.5 rounded-full bg-zinc-600 typing-dot"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-zinc-600 typing-dot"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-zinc-600 typing-dot"></div>
             </div>
        </div>
    `;
    chatBox.appendChild(div);
    lucide.createIcons();
    
    requestAnimationFrame(() => {
        div.style.transition = "all 0.3s ease-out";
        div.style.opacity = "1";
        div.style.transform = "translateY(0)";
    });

    scrollToBottom();
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.opacity = "0";
        setTimeout(() => el.remove(), 200);
    }
}

function scrollToBottom() {
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
}

// Function to show a sleek toast notification
function showToast(message) {
    const toast = document.createElement("div");
    
    // Initial hidden state (translated right and invisible)
    toast.className = "flex items-center gap-3 bg-zinc-800/90 backdrop-blur-md border border-zinc-700 shadow-xl text-zinc-200 px-4 py-3 rounded-xl transform translate-x-12 opacity-0 transition-all duration-300 ease-out";
    
    toast.innerHTML = `
        <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
        <span class="text-sm font-medium">${escapeHTML(message)}</span>
    `;
    
    document.getElementById("toastContainer").appendChild(toast);
    lucide.createIcons();
    
    // Trigger animation to slide in and fade in
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.remove("translate-x-12", "opacity-0");
            toast.classList.add("translate-x-0", "opacity-100");
        });
    });
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        // Slide out and fade out
        toast.classList.remove("translate-x-0", "opacity-100");
        toast.classList.add("translate-x-12", "opacity-0");
        
        // Remove from DOM after animation completes
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
