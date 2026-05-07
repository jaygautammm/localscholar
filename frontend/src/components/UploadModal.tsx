import { useState } from "react";

export default function UploadModal({ onClose, onUpload, uploading }) {
  const [selectedFile, setSelectedFile] = useState(null);

  function handleFileChange(e) {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
    } else {
      alert("Please select a valid PDF file");
    }
  }

  function handleSubmit() {
    if (!selectedFile) return;
    onUpload(selectedFile);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-2xl">
        <h2 className="mb-4 text-xl font-bold text-white">Upload PDF</h2>

        <div className="mb-6">
          <label className="block cursor-pointer rounded-2xl border-2 border-dashed border-slate-700 bg-slate-950 p-8 text-center transition hover:border-indigo-500">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className="text-sm text-slate-400">
              {selectedFile ? (
                <span className="text-indigo-300">{selectedFile.name}</span>
              ) : (
                "Click to select PDF"
              )}
            </div>
          </label>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            disabled={uploading}
            className="flex-1 rounded-xl border border-slate-700 px-4 py-2 font-medium text-slate-300 transition hover:bg-slate-800 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || uploading}
            className="flex-1 rounded-xl bg-indigo-500 px-4 py-2 font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
}