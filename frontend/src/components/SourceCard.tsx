import { useState } from "react";

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="rounded-full bg-indigo-500/20 px-2 py-1 text-xs font-medium text-indigo-300">
          Source {source.source_number}
        </span>
        <span className="text-xs text-slate-500">
          Distance: {source.distance?.toFixed?.(3) ?? "N/A"}
        </span>
      </div>

      <div className="space-y-1 text-sm">
        <p className="text-slate-300">
          <span className="font-semibold text-white">File:</span> {source.file}
        </p>
        <p className="text-slate-300">
          <span className="font-semibold text-white">Chapter:</span> {source.chapter}
        </p>
        <p className="text-slate-300">
          <span className="font-semibold text-white">Pages:</span>{" "}
          {source.page_start} - {source.page_end}
        </p>
      </div>

      <div className="mt-3 rounded-xl bg-slate-950 p-3 text-xs leading-6 text-slate-400">
        {expanded ? source.full_text : source.preview}
      </div>

      <button
        onClick={() => setExpanded(!expanded)}
        className="mt-2 text-xs font-medium text-indigo-400 hover:text-indigo-300"
      >
        {expanded ? "Show less" : "Show full text"}
      </button>
    </div>
  );
}