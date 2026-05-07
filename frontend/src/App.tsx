import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import SourcePanel from "./components/SourcePanel";
import TopBar from "./components/TopBar";
import UploadModal from "./components/UploadModal";
import {
  fetchDocuments,
  ingestDocument,
  chatWithDocument,
  uploadPDF,
} from "./services/api";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState("");
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [ingesting, setIngesting] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [status, setStatus] = useState("Ready");

  useEffect(() => {
    async function loadDocuments() {
      try {
        setLoadingDocs(true);
        const data = await fetchDocuments();
        setDocuments(data.documents || []);

        if (data.documents?.length > 0 && !selectedDocument) {
          setSelectedDocument(data.documents[0].file_name);
        }
      } catch (error) {
        console.error(error);
        setStatus("Failed to load documents");
      } finally {
        setLoadingDocs(false);
      }
    }

    loadDocuments();
  }, [selectedDocument]);

  async function handleUpload(file) {
    try {
      setUploading(true);
      setStatus(`Uploading ${file.name}...`);

      const result = await uploadPDF(file);

      setStatus(`Uploaded successfully: ${result.file_name}`);
      setShowUploadModal(false);
      await loadDocuments();
      setSelectedDocument(result.file_name);
    } catch (error) {
      console.error(error);
      setStatus(error.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleIngest({ fileName, maxChars, overlapChars, resetCollection }) {
    try {
      setIngesting(true);
      setStatus(`Ingesting ${fileName}...`);

      const result = await ingestDocument({
        file_name: fileName,
        max_chars: maxChars,
        overlap_chars: overlapChars,
        reset_collection: resetCollection,
      });

      setStatus(`Ingested: ${result.result.chunks_indexed} chunks`);
    } catch (error) {
      console.error(error);
      setStatus(error.message);
    } finally {
      setIngesting(false);
    }
  }

  async function handleSendQuestion(question) {
    const trimmed = question.trim();
    if (!trimmed) return;

    const userMessage = {
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setChatLoading(true);
    setStatus("Thinking...");

    try {
      const result = await chatWithDocument({
        question: trimmed,
        n_results: 5,
        file_name: selectedDocument || null,
      });

      const assistantMessage = {
        role: "assistant",
        content: result.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSources(result.sources || []);
      setStatus("Answer generated");
    } catch (error) {
      console.error(error);

      const assistantMessage = {
        role: "assistant",
        content: `Error: ${error.message}`,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStatus("Chat failed");
    } finally {
      setChatLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <TopBar status={status} />

      <div className="grid grid-cols-12 gap-4 p-4">
        <div className="col-span-3">
          <Sidebar
            documents={documents}
            selectedDocument={selectedDocument}
            setSelectedDocument={setSelectedDocument}
            loadingDocs={loadingDocs}
            ingesting={ingesting}
            onIngest={handleIngest}
            onOpenUpload={() => setShowUploadModal(true)}
          />
        </div>

        <div className="col-span-6">
          <ChatPanel
            messages={messages}
            onSend={handleSendQuestion}
            loading={chatLoading}
          />
        </div>

        <div className="col-span-3">
          <SourcePanel sources={sources} />
        </div>
      </div>

      {showUploadModal && (
        <UploadModal
          onClose={() => setShowUploadModal(false)}
          onUpload={handleUpload}
          uploading={uploading}
        />
      )}
    </div>
  );
}