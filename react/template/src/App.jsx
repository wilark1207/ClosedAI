import React from 'react';
import './App.css'; // Make sure to adjust the path based on your project structure
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const App = () => {
  const sendMessage = () => {
    // Implement logic to send the message to the server
    // and update the chat messages on the client side
  };

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
              <h2 className="title">How can I help?</h2>
            </div>
            <div id="main-chat-screen">
              {/* Your chat UI goes here */}
              <div id="chat-messages">
                {/* Display chat messages here */}
              </div>
              <div className="chatDiv" id="chat-input">
                <input type="text" id="message-input" placeholder="Type your message..." />
                <button className="sendButton" onClick={sendMessage}>
                  <FontAwesomeIcon icon={faPaperPlane} />
                </button>
              </div>
              <div className="suggestionsDiv">
                <a className="suggestion">Am I free next Friday?</a>
                <a className="suggestion">How many hours have I spent studying this week?</a>
                <a className="suggestion">What do I have on today?</a>
              </div>
              <h4>Developed by ClosedAI for UNIHACK 2024. Powered by AI</h4>
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
      </div>
  );
};

export default App;