export default function TopBar({ status }) {
  return (
    <div className="border-b border-slate-800 bg-slate-900 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            LocalScholar
          </h1>
          <p className="text-sm text-slate-400">
            Offline RAG Research Assistant for Long PDFs
          </p>
        </div>

        <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-300">
          {status}
        </div>
      </div>
    </div>
  );
}