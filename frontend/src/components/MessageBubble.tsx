import ReactMarkdown from "react-markdown";

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-md ${
          isUser
            ? "bg-indigo-500 text-white"
            : "border border-slate-800 bg-slate-900 text-slate-100"
        }`}
      >
        <div className="mb-1 text-xs font-semibold uppercase tracking-wide opacity-70">
          {isUser ? "You" : "LocalScholar"}
        </div>

        {isUser ? (
          <div className="whitespace-pre-wrap leading-7">{content}</div>
        ) : (
          <div className="prose prose-invert prose-sm max-w-none leading-7">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}