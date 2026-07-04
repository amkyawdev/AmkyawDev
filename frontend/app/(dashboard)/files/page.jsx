"use client";
import { useState, useEffect } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import { listFiles, uploadFile } from "@/lib/api-client";
import { toast } from "sonner";

export default function FilesPage() {
  const [files, setFiles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => { loadFiles(); }, []);

  const loadFiles = async () => {
    try {
      const data = await listFiles();
      setFiles(data.files || []);
    } catch (error: any) {
      toast.error("Failed to load files");
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      await uploadFile(file);
      toast.success(`Uploaded: ${file.name}`);
      await loadFiles();
    } catch (error: any) {
      toast.error(error.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="flex flex-col h-full">
      <header className="bg-white border-b border-slate-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Files</h2>
            <p className="text-sm text-slate-500">Manage uploaded and generated files</p>
          </div>
          <label className="btn-primary flex items-center gap-2 cursor-pointer">
            {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}Upload
            <input type="file" onChange={handleUpload} className="hidden" />
          </label>
        </div>
      </header>
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="max-w-4xl mx-auto">
          {loading ? (
            <div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
          ) : files.length === 0 ? (
            <div className="text-center py-20">
              <FileText className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-700 mb-2">No files yet</h3>
              <p className="text-slate-500">Upload files or generate code to see them here</p>
            </div>
          ) : (
            <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
              <div className="grid grid-cols-12 gap-4 px-4 py-3 bg-slate-50 text-xs font-medium text-slate-500 uppercase">
                <div className="col-span-5">Name</div>
                <div className="col-span-3">Path</div>
                <div className="col-span-2">Size</div>
                <div className="col-span-2">Modified</div>
              </div>
              {files.map((file: any, i: number) => (
                <div key={i} className="grid grid-cols-12 gap-4 px-4 py-3 border-t border-slate-100 text-sm hover:bg-slate-50">
                  <div className="col-span-5 font-medium text-slate-900 flex items-center gap-2"><FileText className="w-4 h-4 text-slate-400" />{file.name}</div>
                  <div className="col-span-3 text-slate-500 font-mono text-xs truncate">{file.path}</div>
                  <div className="col-span-2 text-slate-500">{formatSize(file.size)}</div>
                  <div className="col-span-2 text-slate-500">{new Date(file.modified).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
