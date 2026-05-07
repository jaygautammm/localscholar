import SourceCard from "./SourceCard";

export default function SourcePanel({ sources }) {
  return (
    <div className="h-[80vh] rounded-2xl border border-slate-800 bg-slate-950 p-4 shadow-xl flex flex-col">
      <h2 className="mb-4 text-lg font-semibold text-white flex-shrink-0">Retrieved Sources</h2>

      {sources.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-700 p-4 text-sm text-slate-500 flex-1">
          Sources used for the answer will appear here.
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto pr-1 space-y-3">
          {sources.map((source) => (
            <SourceCard
              key={`${source.source_number}-${source.page_start}-${source.chapter}`}
              source={source}
            />
          ))}
        </div>
      )}
    </div>
  );
}