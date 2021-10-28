import { useState } from "react";
import "./App.css";

function App() {
  const [allMessages, setAllMessages] = useState([
    { id: 1, date: "28/10/21", message: "Whats up?" },
    { id: 2, date: "28/10/21", message: "Hi!" },
  ]);
  const [messageField, setMessageField] = useState("");

  const onSendMessage = (e) => {
    e.preventDefault();

    const newMessage = {
      id: allMessages.length + 1,
      date: "28/10/21",
      message: messageField,
    };

    // Make an API request

    setAllMessages([newMessage, ...allMessages]);
  };

  return (
    <div className="app">
      <h1 className="app-name">
        <img
          src="img/twitter-png.png"
          className="twitter-logo"
          alt="Twitter Logo"
        />
        for Introverts
      </h1>

      <form onSubmit={onSendMessage} className="message-form">
        <textarea
          name="msg"
          id="msg"
          placeholder="Enter your very short message here"
          className="message-field"
          value={messageField}
          onChange={(e) => setMessageField(e.target.value)}
          maxLength="10"
        />

        <div className="message-send">
          <div className="message-chars-remaining">
            {10 - messageField.length} character
            {10 - messageField.length !== 1 ? "s" : ""} left
          </div>
          <button type="submit" className="message-send-btn">
            Send
          </button>
        </div>
      </form>

      <div className="messages-list">
        <h3 className="messages-list-title">Recent Messages</h3>

        {allMessages.map(({ id, date, message }) => (
          <div className="messages-list-msg" key={id}>
            <div className="msg-date">{date}</div>
            <div className="message">{message}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
