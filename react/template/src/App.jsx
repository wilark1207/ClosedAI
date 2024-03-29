import { useEffect, useState, useRef } from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import axios from 'axios';
import { faPaperPlane, faWandMagicSparkles, faUser, faMicrophone, faCirclePlay } from '@fortawesome/free-solid-svg-icons';
import MyCalendar from './Calendar';

const App = () => {
  const [data, setData] = useState([{}]);
  const [message, setMessage] = useState('')
  const [msgArr, setMsgArr] = useState([]);
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetch("/api/data").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/messages');
      const responsejson = await response.json();
      // console.log(responsejson)
      // forEach message content then input
      setMsgArr(responsejson);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  }

  setTimeout(fetchMessages, 2000);

  const sendMessage = async () => {
    // Implement logic to send the message to the server
    // and update the chat messages on the client side
    const msg = JSON.stringify({
      input: message
    })

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/get', {msg});
      await fetchMessages();
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  
  };

  const sendAutoMessage = async (messageAuto) => {
    // Implement logic to send the message to the server
    // and update the chat messages on the client side

    const msg = JSON.stringify({
      input: messageAuto
    })

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/get', {msg});
      // Handle the response if needed
      fetchMessages();
      console.log(response.data);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  
  };

  const scrollToBottom = () => {
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
  useEffect(() => {
    scrollToBottom();
  }, [msgArr]);

  const triggerMic = async () => {
    console.log("clicked microphone");
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        let recognition = new SpeechRecognition();
        
        recognition.onstart = function() {
          document.getElementById('recordingScreen').style.display = 'flex';
        };
        
        recognition.onspeechend = function() {
            document.getElementById('recordingScreen').style.display = 'none';
            console.log("Voice recognition ended.");
            recognition.stop();
        };
        
        recognition.onresult = function(event) {
            console.log(event.results[0][0].transcript);
            let transcript = event.results[0][0].transcript;
            setMessage(transcript);
            console.log("Transcription: " + transcript);
        };
        
        recognition.onerror = function(event) {
            console.error("Speech recognition error", event.error);
        };
        
        recognition.start();
    } else {
        console.log("Browser does not support Speech Recognition");
    }
  };
  const textToSpeech = (text) => {
      // Implement logic to convert text to speech
      let message= new window.SpeechSynthesisUtterance(text);
      speechSynthesis.speak(message);
  }

  return (
    <div>
      <meta charSet="UTF-8" />
      <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />

      <title>Flask Chat App</title>
      {/* Add any additional styles or scripts here */}
        <div className="mainContainer">
          <div className="chatContainer">
            <div className="chatHeader">
              <h2 className="title">Calendar AI Assistant</h2>
            </div>
            <div id="main-chat-screen">
              {/* Your chat UI goes here */}
              <div id='recordingScreen' style={{ position: 'absolute', display: "none", justifyContent: 'center', alignItems: 'center', width: "100%", height: '80%', color: 'black' }}>Recording...</div>
              <div id="chat-messages">
                {/* Display chat messages here */}
              
                <div className="messageAI">
                  <span className="icon">
                    <FontAwesomeIcon icon={faWandMagicSparkles} />
                  </span>
                  <div className="content">
                    <h5>AI</h5>
                    <p className="message">How can I assist you today?</p>
                  </div>
                </div>
                {msgArr.map((msg, index) => (
              <div key={index} className={msg.author === 'USER' ? 'messageUser' : 'messageAI'}>
              <span className="icon">
                <FontAwesomeIcon icon={msg.author === 'USER' ? faUser : faWandMagicSparkles} />
              </span>
              <div className="content">
                <h5>{msg.author}</h5>
                <p className="message">{msg.content}</p>
              </div>
              <button style={{ 
                background: 'transparent'
              }} className="speakerButton" onClick={() => textToSpeech(msg.content)}>
                <FontAwesomeIcon icon={faCirclePlay} color='black' className='iconMic' />
              </button>
            </div>
            ))}
                <div ref={messagesEndRef} />
              </div>
              <div className="chatDiv" id="chat-input">
                <div style={{ position: "relative", width: "100%", display: "flex", height: "100%", alignItems: "center", flexDirection: "row" }}>
                  <input type="text" id="message-input" value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message..." />
                  <button className="micButton" onClick={triggerMic}>
                    <FontAwesomeIcon icon={faMicrophone} color='black' className='iconMic' />
                  </button>
                </div>
                <button className="sendButton" onClick={sendMessage}>
                  <FontAwesomeIcon icon={faPaperPlane} />
                </button> 
              </div>
              <div className="suggestionsDiv">
                <a className="suggestion" onClick={() => {
                  sendAutoMessage("Am I free next Friday?")
                }} onChange={e => setMessage(e.target.value)}>Am I free next Friday?</a>
                <a className="suggestion" onClick={() => {
                  sendAutoMessage("How many hours have I spent studying this week?")
                }}onChange={e => setMessage(e.target.value)}>How many hours have I spent studying this week?</a>
                <a className="suggestion" onClick={() => {
                sendAutoMessage("What do I have on today?") 
                }}onChange={e => setMessage(e.target.value)}>What do I have on today?</a>
              </div>
            </div>
          </div>
          <div className="display">
            <div className="displayHeader">
              <h2 className="displayHeaderTitle">March, 2024</h2>
              <h3 className="description">Synced to Google Calendar</h3>
              <MyCalendar />
            </div>
          </div>
        </div>

        {/* Add any additional scripts here */}
      <h4>Developed by ClosedAI for UNIHACK 2024. Powered by AI</h4>
    </div>
  );
};

export default App;
