// API Base URL
const API_BASE = 'http://localhost:8000/api';

// Session ID for chat history
const SESSION_ID = 'session_' + Date.now();

// DOM Elements
const uploadBtn = document.getElementById('uploadBtn');
const csvFileInput = document.getElementById('csvFileInput');
const uploadStatus = document.getElementById('uploadStatus');
const uploadSection = document.getElementById('uploadSection');
const csvInfoSection = document.getElementById('csvInfoSection');
const csvInfo = document.getElementById('csvInfo');
const chatSection = document.getElementById('chatSection');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const clearChatBtn = document.getElementById('clearChatBtn');
const viewPreviewBtn = document.getElementById('viewPreviewBtn');
const previewModal = document.getElementById('previewModal');
const closePreviewBtn = document.getElementById('closePreviewBtn');
const previewContent = document.getElementById('previewContent');

// Event Listeners
uploadBtn.addEventListener('click', () => csvFileInput.click());
csvFileInput.addEventListener('change', handleFileUpload);
sendBtn.addEventListener('click', sendMessage);
clearChatBtn.addEventListener('click', clearChatHistory);
viewPreviewBtn.addEventListener('click', showPreview);
closePreviewBtn.addEventListener('click', () => previewModal.classList.remove('show'));

// Handle Enter key in chat input
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize chat input
chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = chatInput.scrollHeight + 'px';
});

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
        showUploadStatus('Only CSV files are allowed', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    showUploadStatus('Uploading...', 'loading');

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const data = await response.json();
        showUploadStatus(`File "${data.filename}" uploaded successfully!`, 'success');
        
        // Display CSV info
        displayCSVInfo(data.info);
        
        // Show sections
        setTimeout(() => {
            csvInfoSection.style.display = 'block';
            chatSection.style.display = 'block';
            uploadSection.style.display = 'none';
        }, 1000);

    } catch (error) {
        showUploadStatus(`Error: ${error.message}`, 'error');
    }
}

// Show upload status
function showUploadStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `upload-status ${type}`;
}

// Display CSV information
function displayCSVInfo(info) {
    const items = [
        { label: 'Filename', value: info.filename },
        { label: 'Rows', value: info.rows.toLocaleString() },
        { label: 'Columns', value: info.columns.toLocaleString() },
        { label: 'Memory Usage', value: info.memory_usage }
    ];

    const html = items.map(item => `
        <div class="info-item">
            <span class="info-label">${item.label}:</span>
            <span class="info-value">${item.value}</span>
        </div>
    `).join('');

    csvInfo.innerHTML = html;
}

// Show data preview
async function showPreview() {
    try {
        const response = await fetch(`${API_BASE}/csv-preview?rows=10`);
        if (!response.ok) throw new Error('Failed to fetch preview');

        const data = await response.json();
        displayPreview(data.preview);
        previewModal.classList.add('show');

    } catch (error) {
        alert(`Error loading preview: ${error.message}`);
    }
}

// Display preview table
function displayPreview(preview) {
    if (!preview || preview.length === 0) {
        previewContent.innerHTML = '<p>No data to display</p>';
        return;
    }

    const columns = Object.keys(preview[0]);
    
    let html = '<table class="preview-table">';
    
    // Header
    html += '<thead><tr>';
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead>';
    
    // Body
    html += '<tbody>';
    preview.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            html += `<td>${row[col] !== null ? row[col] : ''}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table>';
    
    previewContent.innerHTML = html;
}

// Send chat message
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Disable input
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: SESSION_ID
            })
        });

        if (!response.ok) throw new Error('Failed to get response');

        const data = await response.json();
        addMessage(data.response, 'assistant');

    } catch (error) {
        addMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        // Re-enable input
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Add message to chat
function addMessage(text, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = text;
    
    contentDiv.appendChild(p);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Clear chat history
async function clearChatHistory() {
    if (!confirm('Are you sure you want to clear the chat history?')) return;

    try {
        const response = await fetch(`${API_BASE}/clear-history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: SESSION_ID
            })
        });

        if (!response.ok) throw new Error('Failed to clear history');

        // Clear messages except the first welcome message
        chatMessages.innerHTML = `
            <div class="message assistant-message">
                <div class="message-content">
                    <p>Hello! I'm ready to help you analyze your CSV data. What would you like to know?</p>
                </div>
            </div>
        `;

    } catch (error) {
        alert(`Error clearing history: ${error.message}`);
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === previewModal) {
        previewModal.classList.remove('show');
    }
});
