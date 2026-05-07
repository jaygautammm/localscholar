import { useState } from "react";

export default function Sidebar({
  documents,
  selectedDocument,
  setSelectedDocument,
  loadingDocs,
  ingesting,
  onIngest,
  onOpenUpload,
}) {
  const [maxChars, setMaxChars] = useState(1200);
  const [overlapChars, setOverlapChars] = useState(150);
  const [resetCollection, setResetCollection] = useState(false);

  function handleSubmit() {
    if (!selectedDocument) return;

    onIngest({
      fileName: selectedDocument,
      maxChars: Number(maxChars),
      overlapChars: Number(overlapChars),
      resetCollection,
    });
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-xl">
      <h2 className="mb-4 text-lg font-semibold text-white">Document Control</h2>

      <button
        onClick={onOpenUpload}
        className="mb-4 w-full rounded-xl border border-emerald-500/50 bg-emerald-500/10 px-4 py-2 font-medium text-emerald-300 transition hover:bg-emerald-500/20"
      >
        + Upload New PDF
      </button>

      <div className="mb-4">
        <label className="mb-2 block text-sm text-slate-400">Available PDFs</label>

        {loadingDocs ? (
          <p className="text-sm text-slate-500">Loading documents...</p>
        ) : (
          <select
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
            value={selectedDocument}
            onChange={(e) => setSelectedDocument(e.target.value)}
          >
            <option value="">Select a document</option>
            {documents.map((doc) => (
              <option key={doc.file_name} value={doc.file_name}>
                {doc.file_name}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-2 block text-sm text-slate-400">Max Chunk Size</label>
        <input
          type="number"
          value={maxChars}
          onChange={(e) => setMaxChars(e.target.value)}
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
        />
      </div>

      <div className="mb-4">
        <label className="mb-2 block text-sm text-slate-400">Overlap Size</label>
        <input
          type="number"
          value={overlapChars}
          onChange={(e) => setOverlapChars(e.target.value)}
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
        />
      </div>

      <label className="mb-4 flex items-center gap-2 text-sm text-slate-300">
        <input
          type="checkbox"
          checked={resetCollection}
          onChange={(e) => setResetCollection(e.target.checked)}
        />
        Reset collection before ingest
      </label>

      <button
        onClick={handleSubmit}
        disabled={!selectedDocument || ingesting}
        className="w-full rounded-xl bg-indigo-500 px-4 py-2 font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {ingesting ? "Ingesting..." : "Ingest Document"}
      </button>

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-3">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          💡 Pro Tip
        </h3>
        <p className="text-xs leading-5 text-slate-500">
          Smaller chunks improve precision. Larger chunks preserve context. Test both for your use case.
        </p>
      </div>
    </div>
  );
}