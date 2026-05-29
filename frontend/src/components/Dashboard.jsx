import React, { useState, useEffect } from "react";

const API_BASE_URL = "https://a791-2404-8000-1024-4b21-1fd-950c-b0f1-1ee9.ngrok-free.app/api/v1";

// Fungsi helper dipisahkan di luar komponen agar tidak dibuat ulang tiap render
const getPlatformTag = (url) => {
  if (!url) return "Web";
  const lowerUrl = url.toLowerCase();
  if (lowerUrl.includes("amazon")) return "Amazon";
  if (lowerUrl.includes("ebay")) return "eBay";
  if (lowerUrl.includes("shopee")) return "Shopee";
  if (lowerUrl.includes("tokopedia")) return "Tokopedia";
  return "External";
};

const Dashboard = () => {
  // --- States ---
  const [messages, setMessages] = useState([]);
  const [targetUrl, setTargetUrl] = useState("");
  const [targetComponent, setTargetComponent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [activeTasks, setActiveTasks] = useState([]);
  const [taskHistory, setTaskHistory] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  // UI & UX States
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);
  const [isHistoryError, setIsHistoryError] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");
  const [sortOrder, setSortOrder] = useState("newest");
  const [limit, setLimit] = useState(20);
  const [hasMore, setHasMore] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Persistence (LocalStorage)
  const [bookmarkedTasks, setBookmarkedTasks] = useState(() => {
    const saved = localStorage.getItem("bh_bookmarks");
    return saved ? JSON.parse(saved) : [];
  });

  // --- Effects ---
  useEffect(() => {
    fetchTaskHistory();
  }, [limit]);

  useEffect(() => {
    localStorage.setItem("bh_bookmarks", JSON.stringify(bookmarkedTasks));
  }, [bookmarkedTasks]);

  // Polling for active tasks
  useEffect(() => {
    if (activeTasks.length === 0) return;

    const interval = setInterval(async () => {
      const updatedTasks = await Promise.all(
        activeTasks.map(async (taskId) => {
          try {
            const response = await fetch(`${API_BASE_URL}/surveillance/task/${taskId}`, {
              headers: { "ngrok-skip-browser-warning": "69420" }
            });
            if (!response.ok) return { id: taskId, status: 'error' };
            return await response.json();
          } catch {
            return { id: taskId, status: 'error' };
          }
        })
      );

      updatedTasks.forEach((task) => {
        if (task.status === "completed" || task.status === "failed") {
          setActiveTasks((prev) => prev.filter((id) => id !== task.id));
          fetchTaskHistory(true);
          if (selectedTaskId === task.id || !selectedTaskId) {
            displayTaskResult(task);
          }
        }
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [activeTasks, selectedTaskId]);

  // --- Actions ---
  const fetchTaskHistory = async (silent = false) => {
    if (!silent) setIsHistoryLoading(true);
    setIsHistoryError(false);
    try {
      const response = await fetch(`${API_BASE_URL}/surveillance/tasks?limit=${limit}`, {
        headers: {
          "ngrok-skip-browser-warning": "69420"
        }
      });
      if (response.ok) {
        const data = await response.json();
        setTaskHistory(data);
        setHasMore(data.length >= limit);
      } else {
        setIsHistoryError(true);
      }
    } catch (error) {
      setIsHistoryError(true);
    } finally {
      if (!silent) setIsHistoryLoading(false);
    }
  };

  const handlePullToRefresh = async () => {
    setIsRefreshing(true);
    await fetchTaskHistory(true);
    setTimeout(() => setIsRefreshing(false), 800);
  };

  const renderProductGallery = (products) => {
    if (!products || products.length === 0) return "";

    return `
      <div class="mt-8">
        <h4 class="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
          <i class="fa-solid fa-store text-blue-600"></i> Marketplace Data Extraction
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          ${products.slice(0, 6).map(p => `
            <div class="bg-white border border-slate-200 rounded-xl p-3 flex gap-3 items-center hover:border-blue-300 transition-colors shadow-sm">
              <div class="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center text-slate-400 shrink-0">
                <i class="fa-solid fa-box text-lg"></i>
              </div>
              <div class="min-w-0">
                <p class="text-[11px] font-bold text-slate-900 truncate">${p.name || 'Unknown Product'}</p>
                <p class="text-[10px] font-black text-blue-600 mt-0.5">$${p.price || 'N/A'}</p>
                <div class="flex items-center gap-1 mt-1">
                   <i class="fa-solid fa-star text-[8px] text-amber-400"></i>
                   <span class="text-[8px] font-bold text-slate-500">${p.rating || 'No Rating'}</span>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
        ${products.length > 6 ? `<p class="text-[10px] text-slate-400 mt-2 font-medium italic">+ ${products.length - 6} more items analyzed...</p>` : ''}
      </div>
    `;
  };

  const displayTaskResult = (task) => {
    let content = "";
    if (task.status === "completed" && task.result_data) {
      try {
        const result = JSON.parse(task.result_data);
        const isMaintain = result.decision === 'MAINTAIN POSITION';
        const analysis = result.market_analysis || {};

        content = `
          <div class="space-y-6">
            <div class="flex items-center gap-3">
              <div class="px-4 py-2 rounded-full border ${isMaintain ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-amber-50 text-amber-700 border-amber-200'} text-[11px] font-bold uppercase tracking-widest flex items-center gap-2">
                <i class="fa-solid ${isMaintain ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i>
                ${result.decision || 'AUDIT_COMPLETE'}
              </div>
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Task ID: #${task.id}</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
               <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
                  <div class="w-8 h-8 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-3">
                    <i class="fa-solid fa-tag text-sm"></i>
                  </div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Cheapest Found</p>
                  <p class="text-lg font-black text-slate-900">$${analysis.cheapest?.price || 'N/A'}</p>
                  <p class="text-[10px] text-slate-500 truncate mt-1">${analysis.cheapest?.name || '---'}</p>
               </div>
               <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
                  <div class="w-8 h-8 bg-amber-100 text-amber-600 rounded-lg flex items-center justify-center mb-3">
                    <i class="fa-solid fa-star text-sm"></i>
                  </div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Top Rated</p>
                  <p class="text-lg font-black text-slate-900">${analysis.best?.rating || 'N/A'}</p>
                  <p class="text-[10px] text-slate-500 truncate mt-1">${analysis.best?.name || '---'}</p>
               </div>
               <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 shadow-sm">
                  <div class="w-8 h-8 ${result.price_anomaly ? 'bg-red-100 text-red-600' : 'bg-emerald-100 text-emerald-600'} rounded-lg flex items-center justify-center mb-3">
                    <i class="fa-solid fa-shield-virus text-sm"></i>
                  </div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase mb-1">Position Health</p>
                  <p class="text-sm font-black ${result.price_anomaly ? 'text-red-600' : 'text-emerald-600'}">
                    ${result.price_anomaly ? 'ANOMALY DETECTED' : 'SECURE POSITION'}
                  </p>
                  <p class="text-[10px] text-slate-500 mt-1">${result.price_anomaly ? 'Action Required' : 'Aligned with Market'}</p>
               </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-md relative overflow-hidden">
               <div class="absolute top-0 right-0 w-32 h-32 bg-blue-50 -mr-16 -mt-16 rounded-full opacity-50"></div>
               <h4 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-3 relative z-10">Strategic Action Path</h4>
               <p class="text-lg font-bold text-slate-900 leading-relaxed italic relative z-10">
                 "${result.recommendation}"
               </p>
            </div>

            ${renderProductGallery(result.extracted_products)}
          </div>
        `;
      } catch (e) {
        content = `<div class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm font-medium">Error: Failed to render visual report.</div>`;
      }
    } else if (task.status === "failed") {
      content = `<div class="bg-red-50 border border-red-100 p-8 rounded-3xl text-center">
        <div class="w-16 h-16 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <i class="fa-solid fa-circle-xmark text-2xl"></i>
        </div>
        <h4 class="font-bold text-slate-900 mb-2">Surveillance Blocked</h4>
        <p class="text-slate-500 text-sm mb-6">Marketplace security measures obstructed the data extraction node.</p>
        <button onclick="window.location.reload()" class="px-6 py-2 bg-slate-900 text-white font-bold text-xs rounded-lg uppercase tracking-widest">Retry Connection</button>
      </div>`;
    } else {
      content = `<div class="flex flex-col items-center justify-center py-20 bg-slate-50 rounded-3xl border border-dashed border-slate-300">
        <div class="w-20 h-20 bg-white shadow-xl rounded-full flex items-center justify-center mb-6 relative">
           <i class="fa-solid fa-satellite-dish text-2xl text-blue-600 animate-pulse"></i>
           <div class="absolute inset-0 border-4 border-blue-100 rounded-full animate-ping"></div>
        </div>
        <h4 class="font-bold text-slate-900 mb-1">Analyzing Marketplace Node...</h4>
        <p class="text-slate-400 text-xs font-medium uppercase tracking-widest">${task.status.replace(/_/g, ' ')}</p>
      </div>`;
    }

    setMessages([
      { role: "user", content: `Reviewing audit for <span class="text-blue-600 font-bold">${task.target_component}</span>` },
      { role: "assistant", content: content, task: task }
    ]);
  };

  const handleTaskClick = (task) => {
    setSelectedTaskId(task.id);
    displayTaskResult(task);
    if (window.innerWidth < 1024) setIsSidebarOpen(false);
  };

  const handleNewAudit = () => {
    setSelectedTaskId(null);
    setMessages([]);
    setTargetUrl("");
    setTargetComponent("");
    if (window.innerWidth < 1024) setIsSidebarOpen(false);
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!targetUrl.trim() || !targetComponent.trim()) return;

    const currentUrl = targetUrl;
    const currentComponent = targetComponent;

    setMessages([{ role: "user", content: `Initiating real-time audit for: <strong class="text-blue-600">${currentComponent}</strong>` }]);
    setTargetUrl("");
    setTargetComponent("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/surveillance/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
        body: JSON.stringify({ target_url: currentUrl, target_component: currentComponent }),
      });
      if (!response.ok) throw new Error("Connection failed");
      const data = await response.json();
      setActiveTasks((prev) => [...prev, data.task_id]);
      setSelectedTaskId(data.task_id);
      setMessages((prev) => [...prev, { role: "assistant", content: `<div class="flex items-center gap-3 p-4 bg-blue-50 border border-blue-100 rounded-2xl text-blue-700 font-bold text-sm"><i class="fa-solid fa-spinner fa-spin"></i> Initializing AI Surveillance Engine #${data.task_id}...</div>` }]);
      fetchTaskHistory(true);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "assistant", content: `<div class="p-4 bg-red-50 text-red-600 font-bold rounded-2xl text-sm">Error: ${error.message}</div>` }]);
    } finally {
      setIsLoading(false);
    }
  };

  // --- Sidebar Logic ---
  const deleteTask = async (taskId, e) => {
    e.stopPropagation();
    if (!confirm("Delete this record permanently?")) return;
    try {
      await fetch(`${API_BASE_URL}/surveillance/task/${taskId}`, {
        method: "DELETE",
        headers: { "ngrok-skip-browser-warning": "69420" }
      });
      setTaskHistory((prev) => prev.filter((t) => t.id !== taskId));
      if (selectedTaskId === taskId) { setSelectedTaskId(null); setMessages([]); }
    } catch { alert("Action failed"); }
  };

  const clearAllHistory = async () => {
    if (!confirm("Wipe all history?")) return;
    try {
      await fetch(`${API_BASE_URL}/surveillance/tasks`, {
        method: "DELETE",
        headers: { "ngrok-skip-browser-warning": "69420" }
      });
      setTaskHistory([]); setSelectedTaskId(null); setMessages([]);
    } catch { alert("Action failed"); }
  };

  const toggleBookmark = (taskId, e) => {
    e.stopPropagation();
    setBookmarkedTasks(prev =>
      prev.includes(taskId) ? prev.filter(id => id !== taskId) : [...prev, taskId]
    );
  };

  const editTaskName = (taskId, e) => {
    e.stopPropagation();
    const task = taskHistory.find(t => t.id === taskId);
    const newName = prompt("Rename this audit:", task.target_component);
    if (newName && newName !== task.target_component) {
      setTaskHistory(prev => prev.map(t => t.id === taskId ? { ...t, target_component: newName } : t));
    }
  };

  const exportHistory = () => {
    const blob = new Blob([JSON.stringify(taskHistory, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "bh_audit_export.json"; a.click();
  };

  const downloadReport = (task) => {
    const content = `Report ID: ${task.id}\nComponent: ${task.target_component}\nURL: ${task.target_url}\nData: ${task.result_data}`;
    const blob = new Blob([content], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = `audit_${task.id}.txt`; a.click();
  };

  const copyReport = (task) => {
    navigator.clipboard.writeText(task.result_data || "No data");
    alert("Copied to clipboard");
  };

  const printReport = () => window.print();

  // --- Filtering & Sorting ---
  const getStatusBadge = (task) => {
    if (task.status !== 'completed') {
      return `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-blue-50 text-blue-600 text-[7px] font-black uppercase tracking-tighter border border-blue-100"><i class="fa-solid fa-sync fa-spin"></i> Syncing</span>`;
    }
    try {
      const result = JSON.parse(task.result_data);
      if (result.price_anomaly) {
        return `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-red-50 text-red-600 text-[7px] font-black uppercase tracking-tighter border border-red-100"><i class="fa-solid fa-triangle-exclamation"></i> Anomaly</span>`;
      }
      return `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-600 text-[7px] font-black uppercase tracking-tighter border border-emerald-100"><i class="fa-solid fa-check"></i> Healthy</span>`;
    } catch {
      return `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-slate-50 text-slate-400 text-[7px] font-black uppercase tracking-tighter border border-slate-200"><i class="fa-solid fa-file-lines"></i> Report</span>`;
    }
  };

  const filteredHistory = taskHistory
    .filter((task) => {
      const matchesSearch = task.target_component.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesFilter = filterStatus === "all" || task.status === filterStatus;
      const matchesBookmark = filterStatus === "bookmarked" ? bookmarkedTasks.includes(task.id) : true;
      return matchesSearch && matchesFilter && matchesBookmark;
    })
    .sort((a, b) => {
      if (sortOrder === "newest") return new Date(b.created_at) - new Date(a.created_at);
      if (sortOrder === "alphabetical") return a.target_component.localeCompare(b.target_component);
      return 0;
    });

  const highlightText = (text) => {
    if (!searchQuery) return text;
    const parts = text.split(new RegExp(`(${searchQuery})`, "gi"));
    return parts.map((p, i) => p.toLowerCase() === searchQuery.toLowerCase() ? <mark key={i} className="bg-blue-100 text-blue-700 font-bold px-0.5 rounded">{p}</mark> : p);
  };

  return (
    <div className="flex h-screen bg-white text-slate-800 font-sans overflow-hidden">

      {/* ── SIDEBAR ── */}
      {isSidebarOpen && (
        <div className="fixed inset-0 bg-slate-900/40 z-40 lg:hidden backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)}></div>
      )}

      <aside className={`
        fixed inset-y-0 left-0 z-50 w-80 bg-slate-50 border-r border-slate-200 flex flex-col transition-transform duration-300 
        ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
        lg:relative lg:translate-x-0
      `}>
        {/* Header */}
        <div className="p-6 bg-white border-b border-slate-200 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2">
            <i className="fa-solid fa-bullseye text-blue-600 text-xl"></i>
            <span className="font-bold text-lg tracking-tight">BargainHunter</span>
          </a>
          <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden text-slate-400 hover:text-slate-900"><i className="fa-solid fa-xmark text-lg"></i></button>
        </div>

        {/* New Audit */}
        <div className="p-4">
          <button
            onClick={handleNewAudit}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white font-bold text-sm rounded-xl hover:bg-blue-700 shadow-lg shadow-blue-500/20 transition-all active:scale-95"
          >
            <i className="fa-solid fa-plus"></i> New Surveillance
          </button>
        </div>

        {/* Filters */}
        <div className="px-4 pb-4 space-y-2 border-b border-slate-200">
          <div className="relative group">
            <i className="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
            <input
              type="text" placeholder="Search history..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs font-medium focus:ring-2 ring-blue-50 focus:border-blue-300 outline-none transition-all"
            />
          </div>
          <div className="flex gap-2">
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="flex-1 bg-white border border-slate-200 rounded-xl text-[10px] font-bold px-3 py-2 outline-none">
              <option value="all">All Records</option>
              <option value="completed">Completed</option>
              <option value="bookmarked">Bookmarked</option>
            </select>
            <button onClick={handlePullToRefresh} className={`px-3 border border-slate-200 rounded-xl bg-white hover:bg-slate-50 ${isRefreshing ? 'animate-spin' : ''}`}>
              <i className="fa-solid fa-rotate-right text-[10px] text-slate-500"></i>
            </button>
          </div>
        </div>

        {/* List History */}
        <div className="flex-1 overflow-y-auto px-2 py-4 space-y-1">
          {isHistoryLoading && taskHistory.length === 0 ? (
            Array(5).fill(0).map((_, i) => <div key={i} className="h-14 w-full bg-slate-200 animate-pulse rounded-2xl mb-2"></div>)
          ) : filteredHistory.map((task) => {
            const platform = getPlatformTag(task.target_url);

            return (
              <div
                key={task.id}
                onClick={() => handleTaskClick(task)}
                // Menambahkan detail text tooltip bawaan saat kursor diarahkan ke komponen ini
                title={`Component: ${task.target_component}\nURL: ${task.target_url}\nDate: ${new Date(task.created_at).toLocaleString()}`}
                className={`group mx-2 flex flex-col gap-1.5 px-3 py-3 rounded-xl cursor-pointer transition-all border ${selectedTaskId === task.id ? 'bg-white shadow-md border-blue-200 ring-2 ring-blue-50' : 'border-transparent hover:bg-slate-200/40'
                  }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${task.status === 'completed' ? 'bg-emerald-500' : task.status === 'failed' ? 'bg-red-500' : 'bg-blue-500 animate-pulse'}`}></div>
                  <p className="flex-1 text-[11px] font-bold text-slate-800 truncate uppercase tracking-tight">{highlightText(task.target_component)}</p>
                  <div dangerouslySetInnerHTML={{ __html: getStatusBadge(task) }} />
                </div>

                <div className="flex items-center justify-between pl-3">
                  <div className="flex items-center gap-1.5 text-slate-400">
                    <i className="fa-solid fa-calendar-day text-[8px]"></i>
                    <span className="text-[8px] font-black uppercase tracking-widest">{new Date(task.created_at).toLocaleDateString()}</span>
                  </div>

                  {/* Komponen Badge Tag Platform */}
                  <span className={`text-[8px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider border ${platform === 'Amazon'
                      ? 'bg-amber-50 text-amber-700 border-amber-200'
                      : platform === 'External'
                        ? 'bg-slate-100 text-slate-600 border-slate-200'
                        : 'bg-blue-50 text-blue-700 border-blue-200'
                    }`}>
                    {platform}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 bg-white">
          <button onClick={clearAllHistory} className="w-full py-2.5 text-[10px] font-bold text-slate-400 hover:text-red-600 uppercase tracking-widest transition-colors">Clear History</button>
        </div>
      </aside>

      {/* ── MAIN ── */}
      <main className="flex-1 flex flex-col relative bg-white">

        {/* Header */}
        <header className="h-20 border-b border-slate-100 flex items-center px-8 md:px-12 justify-between shrink-0">
          <div className="flex items-center gap-6">
            <button onClick={() => setIsSidebarOpen(true)} className="lg:hidden p-2 text-slate-400 hover:text-slate-900"><i className="fa-solid fa-bars-staggered text-xl"></i></button>
            <div className="flex flex-col">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight leading-none mb-1">Compliance Control</h2>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Market Node: Active</span>
              </div>
            </div>
          </div>

          <div className="hidden sm:flex items-center gap-2">
            {selectedTaskId && (
              <>
                <button onClick={() => downloadReport(taskHistory.find(t => t.id === selectedTaskId))} className="w-10 h-10 rounded-xl hover:bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 hover:text-blue-600 transition-all"><i className="fa-solid fa-download"></i></button>
                <button onClick={printReport} className="w-10 h-10 rounded-xl hover:bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 hover:text-blue-600 transition-all"><i className="fa-solid fa-print"></i></button>
                <button onClick={() => copyReport(taskHistory.find(t => t.id === selectedTaskId))} className="w-10 h-10 rounded-xl hover:bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 hover:text-blue-600 transition-all"><i className="fa-solid fa-copy"></i></button>
              </>
            )}
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto pt-8 pb-40 scroll-smooth bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]">
          <div className="max-w-3xl mx-auto px-6">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 text-center animate-fade-in">
                <div className="w-14 h-14 bg-white shadow-md border border-slate-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6">
                  <i className="fa-solid fa-robot text-xl"></i>
                </div>

                {/* Amazon Disclaimer */}
                <div className="mb-8 p-4 bg-white/80 backdrop-blur-sm border border-amber-200 rounded-xl max-w-md mx-auto flex items-center gap-3 text-left shadow-sm">
                  <div className="w-8 h-8 shrink-0 bg-amber-50 text-amber-600 rounded-lg flex items-center justify-center">
                    <i className="fa-brands fa-amazon text-sm"></i>
                  </div>
                  <div>
                    <h4 className="text-[10px] font-black text-amber-800 uppercase tracking-widest">Optimized for Amazon</h4>
                    <p className="text-[11px] text-amber-700 leading-tight font-medium">Use Amazon.com product URLs for maximum data structural integrity.</p>
                  </div>
                </div>

                <h3 className="text-2xl font-bold text-slate-900 mb-2 tracking-tight">Deploy Surveillance</h3>
                <p className="text-slate-500 font-medium max-w-sm mx-auto text-xs leading-relaxed mb-8">Enter target parameters to execute an automated audit workflow.</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-md">
                  <div className="p-4 bg-white rounded-xl text-left border border-slate-100 shadow-sm hover:border-blue-200 transition-colors">
                    <i className="fa-solid fa-magnifying-glass-chart text-blue-600 mb-2 block text-sm"></i>
                    <p className="font-bold text-slate-900 text-[11px] uppercase tracking-tight">Monitoring</p>
                    <p className="text-[10px] text-slate-400 leading-tight">Track competitive pricing and stock levels.</p>
                  </div>
                  <div className="p-4 bg-white rounded-xl text-left border border-slate-100 shadow-sm hover:border-emerald-200 transition-colors">
                    <i className="fa-solid fa-shield-check text-emerald-600 mb-2 block text-sm"></i>
                    <p className="font-bold text-slate-900 text-[11px] uppercase tracking-tight">Guard</p>
                    <p className="text-[10px] text-slate-400 leading-tight">Ensure pricing stays within B2B margins.</p>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className="mb-12 animate-slide-up group">
                  <div className="flex items-start gap-6">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 shadow-lg ${msg.role === 'user' ? 'bg-white text-slate-900 border border-slate-200' : 'bg-blue-600 text-white'
                      }`}>
                      <i className={`fa-solid ${msg.role === 'user' ? 'fa-user' : 'fa-bolt-lightning'}`}></i>
                    </div>
                    <div className="flex-1 pt-2 min-w-0">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{msg.role === 'user' ? 'Operator Command' : 'Audit Intelligence Report'}</span>
                        {msg.role === 'assistant' && msg.task && (
                          <div className="flex gap-4 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button onClick={(e) => toggleBookmark(msg.task.id, e)} className={`text-[10px] font-bold uppercase transition-colors ${bookmarkedTasks.includes(msg.task.id) ? 'text-blue-600' : 'text-slate-400 hover:text-blue-600'}`}>
                              {bookmarkedTasks.includes(msg.task.id) ? 'Saved' : 'Save'}
                            </button>
                            <button onClick={() => copyReport(msg.task)} className="text-[10px] font-bold text-slate-400 hover:text-blue-600 uppercase transition-colors">Copy Data</button>
                          </div>
                        )}
                      </div>
                      <div className="text-base text-slate-700 leading-relaxed" dangerouslySetInnerHTML={{ __html: msg.content }} />
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Input Bar */}
        <div className="absolute bottom-0 left-0 right-0 p-6 md:p-10 bg-gradient-to-t from-white via-white/80 to-transparent pointer-events-none">
          <div className="max-w-4xl mx-auto pointer-events-auto">
            <form onSubmit={handleChatSubmit} className="relative">
              <div className="flex flex-col md:flex-row gap-3 bg-white border border-slate-200 rounded-[2rem] p-4 shadow-2xl focus-within:ring-4 ring-blue-50 transition-all">
                <div className="flex-[2] flex items-center px-4">
                  <i className="fa-solid fa-link text-slate-300 mr-4"></i>
                  <input type="text" value={targetUrl} onChange={(e) => setTargetUrl(e.target.value)} placeholder="Target Marketplace URL..." className="w-full py-3 bg-transparent text-sm font-bold focus:outline-none placeholder:text-slate-300" />
                </div>
                <div className="hidden md:block w-px bg-slate-100 h-10 self-center"></div>
                <div className="flex-1 flex items-center px-4">
                  <i className="fa-solid fa-tags text-slate-300 mr-4"></i>
                  <input type="text" value={targetComponent} onChange={(e) => setTargetComponent(e.target.value)} placeholder="Component Name..." className="w-full py-3 bg-transparent text-sm font-bold focus:outline-none placeholder:text-slate-300" />
                </div>
                <button
                  type="submit" disabled={!targetUrl.trim() || !targetComponent.trim() || isLoading}
                  className="bg-blue-600 text-white px-8 py-4 rounded-[1.5rem] font-bold text-sm shadow-xl shadow-blue-500/20 hover:bg-blue-700 disabled:bg-slate-100 disabled:text-slate-300 transition-all active:scale-95 flex items-center justify-center gap-3"
                >
                  {isLoading ? <i className="fa-solid fa-spinner fa-spin"></i> : <i className="fa-solid fa-paper-plane"></i>}
                  Execute
                </button>
              </div>
              <p className="mt-4 text-[10px] text-center text-slate-400 font-bold uppercase tracking-[0.2em]">BargainHunter AI: Real-time marketplace audit node ready.</p>
            </form>
          </div>
        </div>

      </main>
    </div>
  );
};

export default Dashboard;