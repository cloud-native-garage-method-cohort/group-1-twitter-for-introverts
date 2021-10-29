import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [loadingMessages, setLoadingMessages] = useState(true);
  const [allMessages, setAllMessages] = useState([]);
  const [messageField, setMessageField] = useState("");
  const [sending, setSending] = useState(false);
  const [editingMessages, setEditingMessages] = useState(false);

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

    if (!messageField.trim()) return false;
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
      alert("Error sending message");
    }

    setSending(false);
  };

  const onDeleteMessage = async (idToDelete) => {
    try {
      setAllMessages(allMessages.filter(({ id }) => id !== idToDelete));

      await axios.delete(
        `${process.env.REACT_APP_BACKEND_URL}/delete/${idToDelete}`
      );
    } catch (error) {
      alert("Could not delete message");
    }
  };

  return (
    <div className="app">
      <h1 className="app-name">
        <img
          src="img/twitter-png.png"
          className="twitter-logo"
          alt="Twitter Logo"
        />
        for Introverts !
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
          <button
            type="submit"
            className="message-send-btn"
            disabled={sending || !messageField.trim()}
          >
            {sending ? "Sending..." : "Send"}
          </button>
        </div>
      </form>

      <div className="messages-list">
        <h3 className="messages-list-title">
          <div>Recent Messages</div>
          <input
            type="checkbox"
            checked={editingMessages}
            onChange={(e) => setEditingMessages(e.target.checked)}
          />
        </h3>

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
                {editingMessages && (
                  <button
                    className="message-delete"
                    onClick={() => onDeleteMessage(id)}
                  >
                    Delete
                  </button>
                )}
              </div>
            ))}
      </div>
    </div>
  );
}

export default App;
