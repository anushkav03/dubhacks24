// Select necessary elements
const darkModeToggle = document.getElementById('darkModeToggle');
const removedarkMode = document.getElementById('removedarkMode');
const messageInput = document.getElementById('user-input');
const sendMessageButton = document.getElementById('send-btn');
const promptSelectionDiv = document.getElementById('prompt-selection');
const promptButtonsDiv = document.getElementById('prompt-buttons');
const chatBox = document.getElementById('chat-box');

// Keep track of the theme initiation
let themeInitiated = false;

// Function to initiate theme conversation (now sends theme to LLM)
async function initiateThemeConversation(themeMessage) {
    if (!themeInitiated) {
        themeInitiated = true;

        // Send the theme message to the LLM to generate prompts
        const prompts = await fetchPromptsFromLLM(themeMessage);

        // Show prompt selection
        displayPromptChoices(prompts);
    }
}

// Function to fetch prompts from LLM
async function fetchPromptsFromLLM(themeMessage) {
    try {
        const response = await fetch('http://127.0.0.1:8000/generatePrompts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ theme: themeMessage })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.prompts;  // Assuming the API returns a "prompts" array
    } catch (error) {
        console.error('Error fetching prompts from LLM:', error);
        return ['Error generating prompts', 'Please try again later'];  // Default in case of an error
    }
}

// Display the prompt choices as buttons
function displayPromptChoices(prompts) {
    promptSelectionDiv.classList.remove('hidden');  // Show the prompt selection section
    promptButtonsDiv.innerHTML = '';  // Clear any previous prompt buttons

    // Create buttons for each prompt
    prompts.forEach(prompt => {
        const button = document.createElement('button');
        button.textContent = prompt;
        button.classList.add('prompt-button');
        button.onclick = () => handlePromptSelection(prompt);  // Attach event handler to each button
        promptButtonsDiv.appendChild(button);  // Add the button to the prompt-buttons div
    });
}

// Function to handle prompt selection by the user
async function handlePromptSelection(selectedPrompt) {
    updateChatBox('User', `: ${selectedPrompt}`);

    // Hide the prompt selection area after a prompt is selected
    promptSelectionDiv.classList.add('hidden');

    // Send the selected prompt to LLM to generate a paragraph
    const paragraph = await fetchParagraphFromLLM(selectedPrompt);

    // Display the generated paragraph in the chatbox
    updateChatBox('Bot', paragraph);

    // Show recording button after paragraph generation
    const recordButton = document.createElement('button');
    recordButton.textContent = "Start Recording";
    recordButton.classList.add('record-button');
    recordButton.onclick = startRecording;
    chatBox.appendChild(recordButton);  // Add the recording button to the chatbox
}

// Function to fetch a paragraph from the LLM based on the selected prompt
async function fetchParagraphFromLLM(selectedPrompt) {
    try {
        const response = await fetch('http://127.0.0.1:8000/generateParagraph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: selectedPrompt })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.paragraph;  // Assuming the API returns a "paragraph" field
    } catch (error) {
        console.error('Error fetching paragraph from LLM:', error);
        return 'Error generating paragraph. Please try again later.';  // Default error message
    }
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        const recorder = new MediaRecorder(stream);
        let audioChunks = [];

        // Add data chunks to array as recording continues
        recorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        // When recording stops, create an audio Blob and save it
        recorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            saveAudioFile(audioBlob);
        };

        // Start the recording
        recorder.start();

        // Create a "Stop Recording" button when recording starts
        const stopRecordingButton = document.createElement('button');
        stopRecordingButton.textContent = "Stop Recording";
        stopRecordingButton.classList.add('record-button');

        // When the stop button is clicked, stop the recording
        stopRecordingButton.onclick = () => {
            recorder.stop();  // Stop the recording
            stopRecordingButton.remove();  // Remove the stop button from the chatbox
        };

        // Add the stop button to the chatbox
        chatBox.appendChild(stopRecordingButton);
    }).catch(err => {
        console.error('Error accessing microphone:', err);
    });
}

function stopRecording() {
    if (recorder) {
        recorder.stop();
    }
}

function saveAudioFile(blob) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'audio_files/userSpeech.wav';
    link.click();
}

// Event listeners for theme selection
darkModeToggle.addEventListener('click', () => {
    document.body.classList.add('darkmode');
    initiateThemeConversation("You've entered a mysterious theme!");
});

removedarkMode.addEventListener('click', () => {
    document.body.classList.remove('darkmode');
    initiateThemeConversation("You're in a light-hearted theme!");
});

// Update chatbox function to add user and bot messages
// Update chatbox function to add user and bot messages
function updateChatBox(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    // Differentiate between user and bot messages
    if (sender === 'User') {
        messageDiv.classList.add('user');
    } else {
        messageDiv.classList.add('bot');
    }

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('sender');
    senderSpan.textContent = `${sender}: `;

    const messageSpan = document.createElement('span');
    messageSpan.classList.add('message-text');
    messageSpan.textContent = message;

    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(messageSpan);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
}

sendMessageButton.addEventListener('click', async () => {
    const userMessage = messageInput.value.trim();  // Get the user input and trim any extra spaces

    if (userMessage !== '') {
        // Add the user's message to the chatbox
        updateChatBox('User', userMessage);

        // Send the message to the backend ("/postToClaude" FastAPI endpoint)
        try {
            const response = await fetch('http://127.0.0.1:8000/postToClaude', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error('Failed to send message to Claude.');
            }

            const data = await response.json();

            // Assuming the response from the endpoint includes the bot's reply
            updateChatBox('Claude', data.reply);
        } catch (error) {
            console.error('Error:', error);
            updateChatBox('System', 'Error sending message. Please try again.');
        }

        // Clear the input field after sending the message
        messageInput.value = '';
    }
});


