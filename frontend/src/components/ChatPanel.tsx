import { useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatPanel({ messages, onSend, loading }) {
  const [input, setInput] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;

    onSend(input);
    setInput("");
  }

  function copyLastAnswer() {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((m) => m.role === "assistant");

    if (lastAssistantMessage) {
      navigator.clipboard.writeText(lastAssistantMessage.content);
      alert("Answer copied to clipboard");
    }
  }

  return (
    <div className="flex h-[80vh] flex-col rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <div>
          <h2 className="text-lg font-semibold text-white">Chat Workspace</h2>
          <p className="text-sm text-slate-400">
            Ask grounded questions about your indexed PDF.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            onClick={copyLastAnswer}
            className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:bg-slate-800"
          >
            📋 Copy Answer
          </button>
        )}
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
        {messages.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-700 p-6 text-sm text-slate-500">
            Try asking:
            <div className="mt-3 space-y-2">
              <p>• What does Sun Tzu say about deception?</p>
              <p>• What are the five constant factors?</p>
              <p>• What does the book say about prolonged war?</p>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble key={idx} role={msg.role} content={msg.content} />
          ))
        )}

        {loading && (
          <div className="flex items-center gap-3 rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-400">
            <div className="h-2 w-2 animate-bounce rounded-full bg-indigo-500"></div>
            <div className="h-2 w-2 animate-bounce rounded-full bg-indigo-500 delay-100"></div>
            <div className="h-2 w-2 animate-bounce rounded-full bg-indigo-500 delay-200"></div>
            <span>LocalScholar is thinking...</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-slate-800 p-4">
        <div className="flex gap-3">
          <textarea
            rows={3}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the document..."
            className="flex-1 resize-none rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-2xl bg-emerald-500 px-5 py-3 font-medium text-slate-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>
        </div>
        <p className="mt-2 text-xs text-slate-500">Press Enter to send, Shift+Enter for new line</p>
      </form>
    </div>
  );
}