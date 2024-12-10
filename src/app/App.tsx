import React, { useState, useEffect } from "react";
import { YearSelector } from "./components/YearSelector";
import { ProgressBar } from "./components/ProgressBar";
import { LogBox } from "./components/LogBox";
import {
  BookOpenIcon,
  DownloadIcon,
  GithubIcon,
  StopCircleIcon,
  RefreshIcon,
} from "./components/Icons";
import axios from "axios";

import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [blogUrl, setBlogUrl] = useState("");
  const [startYear, setStartYear] = useState(2020);
  const [endYear, setEndYear] = useState(new Date().getFullYear());
  const [populateBetween, setPopulateBetween] = useState(true);
  const [proxies, setProxies] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [logs, setLogs] = useState<string[]>([]);
  const [requestId, setrequestId] = useState<string>("");
  const [taskId, setTaskId] = useState<string>("");
  

  useEffect(() => {
    if (requestId) {
      // Join the room once requestId is available
      console.log(`Joining room: ${requestId}`);
      socket.emit('join_room', { requestId });

      socket.on('progress', (data) => {
        if (data.requestId === requestId) {
          setProgress(data.progress);
        }
      });

      socket.on('log', (data) => {
        if (data.requestId === requestId) {
          setLogs((prevLogs) => [...prevLogs, data.log]);
        }
      });

      socket.on('state', (data) => {
        if (data.requestId === requestId) {
          setIsProcessing(false);
          if (data.state === 'finished_ok') {
            setStatus('success');
          }
          if (data.error) {
            setError(data.state);
          }
        }
      });

      return () => {
        // Leave the room when the component is unmounted or requestId changes
        socket.emit('leave_room', { requestId });
        socket.off('progress');
        socket.off('log');
        socket.off('state');
      };
    }
  }, [isProcessing, requestId]);  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsProcessing(true);
    setProgress(0);
    setStatus("Starting crawler...");
    setLogs([]);

    try {
      const years = [startYear, endYear];
      const response = await axios.post("http://127.0.0.1:5000/api/crawl", {
        blogUrl,
        years,
        populateBetween,
        proxies,
      });
      const requestId = response.data.requestId;
      const taskId = response.data.taskId;
      setrequestId(requestId);
      setTaskId(taskId);
      setStatus("🔄 Processing...");
    } catch (err: any) {
      console.log(err);
      setIsProcessing(false);
      alert("❌ Error occurred during processing: " + err.response.data.message);
    }
  };

  const handleStop = async () => {
    try {
      setStatus("⏹️ Stopping process...");
      const response = await axios.post(`http://127.0.0.1:5000/api/stop/${taskId}`);
      if (response.status === 200) {
        setStatus("⏹️ Process stopped");
        setIsProcessing(false);
      }
    } catch (err) {
      setError("Failed to stop process");
    }
  };

  const handleReset = async () => {
    try {
      await axios.post(`http://127.0.0.1:5000/api/reset/${requestId}`);
      setStatus("");
      setProgress(0);
      setError("");
      setLogs([]);
      setIsProcessing(false);
    } catch (err) {
      setError("Failed to reset");
    }
  };

  const handleDownload = async () => {
    try {
        if (requestId) {
            const url = `http://127.0.0.1:5000/api/download/${requestId}`;
            // download
            const response = await axios.get(url, {
                responseType: "blob",
            });
            const blob = new Blob([response.data], { type: "application/zip" });
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = blobUrl;
            link.download = `${requestId}_blog_data.zip`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);            
        }
    } catch (err) {
        console.error("Error downloading the file:", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BookOpenIcon className="h-8 w-8 text-indigo-600" />
              <h1 className="text-2xl font-bold text-gray-900">Blog Crawler</h1>
            </div>
            <a
              href="https://github.com/sergioparamo/blog-crawler"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-500 hover:text-gray-700"
            >
              <GithubIcon className="h-6 w-6" />
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="blog-url"
                className="block text-sm font-medium text-gray-700"
              >
                Blog URL
              </label>
              <input
                type="url"
                id="blog-url"
                required
                value={blogUrl}
                onChange={(e) => setBlogUrl(e.target.value)}
                placeholder="https://example.com/blog"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <YearSelector
              startYear={startYear}
              endYear={endYear}
              populateBetween={populateBetween}
              proxies={proxies}
              onStartYearChange={setStartYear}
              onEndYearChange={setEndYear}
              onPopulateBetweenChange={setPopulateBetween}
              onProxiesChange={setProxies}
            />

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={isProcessing}
                className="flex-1 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400"
              >
                {isProcessing ? "Processing..." : "Start Crawling"}
              </button>
              {isProcessing && (
                <button
                  type="button"
                  onClick={handleStop}
                  className="flex items-center justify-center py-2 px-4 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50"
                >
                  <StopCircleIcon className="h-4 w-4 mr-2" />
                  Stop
                </button>
              )}
            </div>
          </form>

          {isProcessing && (
            <div className="mt-8">
              <ProgressBar progress={progress} status={status} />
              <LogBox logs={logs} />
            </div>
          )}

          {error && (
            <div className="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {status === "success" && (
          <div className="mt-6 flex justify-center space-x-4">
            <button
              onClick={() => handleDownload()}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <DownloadIcon className="h-4 w-4 mr-2" />
              Download PDFs
            </button>
            <button
              onClick={handleReset}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
            >
              <RefreshIcon className="h-4 w-4 mr-2" />
              Reset
            </button>
          </div>
        )}
        </div>
      </main>
    </div>
  );
}

export default App;