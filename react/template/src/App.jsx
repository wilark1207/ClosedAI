import React, { useEffect, useState, useRef } from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import axios from 'axios';
import { faPaperPlane, faWandMagicSparkles, faUser } from '@fortawesome/free-solid-svg-icons';


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

  useEffect(() => {
    console.log(msgArr);
  }, [msgArr])

  const fetchData = async () => {
    try {
      const response = await fetch('/api/data');
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/messages');
      const responsejson = await response.json();
      //console.log(responsejson)
      setMsgArr(responsejson);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  }

  const sendMessage = async () => {
    // Implement logic to send the message to the server
    // and update the chat messages on the client side

    const msg = JSON.stringify({
      input: message
    })

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/get', {msg});
      // Handle the response if needed
      fetchMessages();
      console.log(response.data);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  
  };
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }
  useEffect(() => {
    scrollToBottom()
  }, [msgArr]);
  return (
    <div>
      <meta charSet="UTF-8" />
      <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />

      <title>Flask Chat App</title>
      {/* Add any additional styles or scripts here */}
      <body>
        <div className="mainContainer">
          <div className="chatContainer">
            <div className="chatHeader">
              <h2 className="title">Calendar AI Assistant</h2>
            </div>
            <div id="main-chat-screen">
              {/* Your chat UI goes here */}
              <div id="chat-messages">
                {/* Display chat messages here */}
              
                <div className="messageAI">
                  <span className="icon">
                    <FontAwesomeIcon icon={faWandMagicSparkles} />
                  </span>
                  <div className="content">
                    <h5>ClosedAI</h5>
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
            </div>
            ))}
                <div ref={messagesEndRef} />
              </div>
              <div className="chatDiv" id="chat-input">
                <input type="text" id="message-input" value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message..." />
                <button className="sendButton" onClick={sendMessage}>
                  <FontAwesomeIcon icon={faPaperPlane} />
                </button> 
              </div>
              <div className="suggestionsDiv">
                <a className="suggestion">Am I free next Friday?</a>
                <a className="suggestion">How many hours have I spent studying this week?</a>
                <a className="suggestion">What do I have on today?</a>
              </div>
            </div>
          </div>
          <div className="display">
            <div className="displayHeader">
              <h2 className="displayHeaderTitle">March, 2024</h2>
              <h3 className="description">Synced to Google Calendar</h3>
            </div>
          </div>
        </div>

        {/* Add any additional scripts here */}
      </body>
      <h4>Developed by ClosedAI for UNIHACK 2024. Powered by AI</h4>
    </div>
  );
};

export default App;
