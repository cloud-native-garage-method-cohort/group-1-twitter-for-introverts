import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [loadingMessages, setLoadingMessages] = useState(true);
  const [allMessages, setAllMessages] = useState([]);
  const [messageField, setMessageField] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    const getMessages = async () => {
      try {
        const { data } = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}`
        );
        setAllMessages(data.messages);
        setLoadingMessages(false);
      } catch (error) {
        alert("Could not load existing messages");
      }
    };

    getMessages();
  }, []);

  const onSendMessage = async (e) => {
    e.preventDefault();
    setSending(true);

    // Make an API request
    try {
      const { data } = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}`,
        {
          message: messageField,
        }
      );

      setAllMessages([data.new_message, ...allMessages]);
      setMessageField("");
    } catch (error) {
      alert("Oh no you screwed something up!");
    }

    setSending(false);
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
          <button type="submit" className="message-send-btn" disabled={sending}>
            {sending ? "Sending..." : "Send"}
          </button>
        </div>
      </form>

      <div className="messages-list">
        <h3 className="messages-list-title">Recent Messages</h3>

        {loadingMessages
          ? "Loading messages..."
          : allMessages.map(({ id, date, message }) => (
              <div className="messages-list-msg" key={id}>
                <div className="msg-date">
                  {new Date(date).toLocaleDateString("en-GB", {
                    year: "numeric",
                    month: "numeric",
                    day: "numeric",
                    hour: "numeric",
                    minute: "numeric",
                  })}
                </div>
                <div className="message">{message}</div>
              </div>
            ))}
      </div>
    </div>
  );
}

export default App;
