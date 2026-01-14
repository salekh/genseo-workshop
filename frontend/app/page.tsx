"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Activity, FileText, Send, Settings, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import dynamic from 'next/dynamic';
import Image from 'next/image';

const MDEditor = dynamic(() => import("@uiw/react-md-editor"), { ssr: false });

// Types
interface LogEvent {
  type: 'status' | 'log' | 'data' | 'error' | 'complete';
  content: any;
  timestamp: string;
}

interface StepStatus {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'completed' | 'error';
}

export default function Home() {
  // State
  const [topic, setTopic] = useState('');
  const [contentType, setContentType] = useState('Blog Post');
  const [targetGroup, setTargetGroup] = useState('General Audience');
  const [language, setLanguage] = useState('German');
  const [location, setLocation] = useState('Germany');
  
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<LogEvent[]>([]);
  const [briefing, setBriefing] = useState<string>('');
  const [steps, setSteps] = useState<StepStatus[]>([
    { id: 'init', label: 'Initialization', status: 'pending' },
    { id: 'research', label: 'Research', status: 'pending' },
    { id: 'parsing', label: 'Content Parsing', status: 'pending' },
    { id: 'analysis', label: 'Semantic Analysis', status: 'pending' },
    { id: 'briefing', label: 'Briefing Generation', status: 'pending' },
    { id: 'evaluation', label: 'Evaluation', status: 'pending' },
  ]);

  const logsEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll logs
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const startMission = async () => {
    setIsRunning(true);
    setLogs([]);
    setBriefing('');
    setSteps(steps.map(s => ({ ...s, status: 'pending' })));

    const queryParams = new URLSearchParams({
      topic,
      content_type: contentType,
      target_group: targetGroup,
      language,
      location,
    });

    const eventSource = new EventSource(`http://localhost:8000/api/mission/stream?${queryParams.toString()}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const timestamp = new Date().toLocaleTimeString();
        let content: any = '';

        // Map backend fields to frontend content
        if (data.message) content = data.message;
        else if (data.data) content = data.data;
        else if (data.report) content = data.report;
        else if (data.content) content = data.content; // Fallback

        if (data.type === 'status') {
          updateStepStatus(content);
          setLogs(prev => [...prev, { type: 'status', content, timestamp }]);
        } else if (data.type === 'log') {
          setLogs(prev => [...prev, { type: 'log', content, timestamp }]);
        } else if (data.type === 'data') {
          if (data.key === 'briefing') {
              setBriefing(content);
          }
          // Optional: Log data events if needed, or just specific ones
          if (data.key === 'keywords' || data.key === 'competitors') {
             setLogs(prev => [...prev, { type: 'data', content: `${data.key}: ${JSON.stringify(content).slice(0, 100)}...`, timestamp }]);
          }
        } else if (data.type === 'complete') {
          setIsRunning(false);
          eventSource.close();
          setSteps(prev => prev.map(s => s.status === 'running' ? { ...s, status: 'completed' } : s));
          setLogs(prev => [...prev, { type: 'complete', content: 'Mission Complete', timestamp }]);
        } else if (data.type === 'error') {
          setLogs(prev => [...prev, { type: 'error', content, timestamp }]);
          // Don't stop on all errors, but maybe specific ones? 
          // For now, let's keep running unless it's a critical failure signal
        }
      } catch (e) {
        console.error('Error parsing SSE event:', e);
      }
    };

    eventSource.onerror = () => {
      setLogs(prev => [...prev, { type: 'error', content: 'Connection lost', timestamp: new Date().toLocaleTimeString() }]);
      setIsRunning(false);
      eventSource.close();
    };
  };

  const updateStepStatus = (message: string) => {
    if (!message || typeof message !== 'string') return;
    
    const lowerMsg = message.toLowerCase();
    let activeStepId = '';

    if (lowerMsg.includes('starting mission')) activeStepId = 'init';
    else if (lowerMsg.includes('research') || lowerMsg.includes('keywords')) activeStepId = 'research';
    else if (lowerMsg.includes('parsing')) activeStepId = 'parsing';
    else if (lowerMsg.includes('semantic analysis')) activeStepId = 'analysis';
    else if (lowerMsg.includes('briefing')) activeStepId = 'briefing';
    else if (lowerMsg.includes('evaluating')) activeStepId = 'evaluation';

    if (activeStepId) {
      setSteps(prev => prev.map(s => {
        if (s.id === activeStepId) return { ...s, status: 'running' };
        if (s.status === 'running' && s.id !== activeStepId) return { ...s, status: 'completed' };
        return s;
      }));
    }
  };

  return (
    <div className="min-h-screen bg-white font-sans text-google-gray-900">
      {/* Header */}
      <header className="border-b border-google-gray-200 bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Image src="/logo.png" alt="GenSEO Logo" width={32} height={32} className="object-contain" />
            <span className="text-xl font-normal text-google-gray-700 tracking-tight">GenSEO</span>
          </div>
          <div className="flex items-center gap-4">
             <div className="w-8 h-8 rounded-full bg-google-blue text-white flex items-center justify-center text-sm font-medium">
                A
             </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Configuration */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white rounded-2xl border border-google-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
              <h2 className="text-lg font-normal text-google-gray-900 mb-6 flex items-center gap-2">
                <Settings className="w-5 h-5 text-google-gray-500" />
                Mission Parameters
              </h2>
              
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-medium text-google-gray-600 mb-1.5 uppercase tracking-wider">Topic / Keyword</label>
                  <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g. Sustainable Coffee"
                    className="w-full px-4 py-3 rounded-lg border border-google-gray-300 focus:border-google-blue focus:ring-2 focus:ring-google-blue/20 outline-none transition-all text-google-gray-900 placeholder:text-google-gray-400"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-medium text-google-gray-600 mb-1.5 uppercase tracking-wider">Content Type</label>
                      <select
                        value={contentType}
                        onChange={(e) => setContentType(e.target.value)}
                        className="w-full px-4 py-3 rounded-lg border border-google-gray-300 focus:border-google-blue focus:ring-2 focus:ring-google-blue/20 outline-none transition-all text-google-gray-900 bg-white"
                      >
                        <option>Blog Post</option>
                        <option>Landing Page</option>
                        <option>Product Description</option>
                        <option>Whitepaper</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-google-gray-600 mb-1.5 uppercase tracking-wider">Language</label>
                      <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full px-4 py-3 rounded-lg border border-google-gray-300 focus:border-google-blue focus:ring-2 focus:ring-google-blue/20 outline-none transition-all text-google-gray-900 bg-white"
                      >
                        <option>German</option>
                        <option>English</option>
                        <option>French</option>
                        <option>Spanish</option>
                      </select>
                    </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-google-gray-600 mb-1.5 uppercase tracking-wider">Target Group</label>
                  <input
                    type="text"
                    value={targetGroup}
                    onChange={(e) => setTargetGroup(e.target.value)}
                    placeholder="e.g. Eco-conscious millennials"
                    className="w-full px-4 py-3 rounded-lg border border-google-gray-300 focus:border-google-blue focus:ring-2 focus:ring-google-blue/20 outline-none transition-all text-google-gray-900 placeholder:text-google-gray-400"
                  />
                </div>

                 <div>
                  <label className="block text-xs font-medium text-google-gray-600 mb-1.5 uppercase tracking-wider">Target Region</label>
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g. Germany"
                    className="w-full px-4 py-3 rounded-lg border border-google-gray-300 focus:border-google-blue focus:ring-2 focus:ring-google-blue/20 outline-none transition-all text-google-gray-900 placeholder:text-google-gray-400"
                  />
                </div>

                <button
                  onClick={startMission}
                  disabled={isRunning || !topic}
                  className={`w-full py-3 px-6 rounded-full font-medium text-sm flex items-center justify-center gap-2 transition-all shadow-sm ${
                    isRunning || !topic
                      ? 'bg-google-gray-100 text-google-gray-400 cursor-not-allowed'
                      : 'bg-google-blue text-white hover:bg-blue-600 hover:shadow-md active:scale-[0.98]'
                  }`}
                >
                  {isRunning ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Processing Mission...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      Start Mission
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Status Tracker */}
             <div className="bg-white rounded-2xl border border-google-gray-200 p-6 shadow-sm">
              <h2 className="text-lg font-normal text-google-gray-900 mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-google-gray-500" />
                Execution Graph
              </h2>
              <div className="space-y-4">
                {steps.map((step, index) => (
                  <div key={step.id} className="relative flex items-center gap-4">
                    {/* Connector Line */}
                    {index < steps.length - 1 && (
                        <div className={`absolute left-[15px] top-8 w-0.5 h-6 ${
                            step.status === 'completed' ? 'bg-google-green' : 'bg-google-gray-200'
                        }`} />
                    )}
                    
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors z-10 ${
                      step.status === 'completed' ? 'bg-google-green border-google-green text-white' :
                      step.status === 'running' ? 'bg-white border-google-blue text-google-blue animate-pulse' :
                      'bg-white border-google-gray-300 text-google-gray-300'
                    }`}>
                      {step.status === 'completed' ? <CheckCircle className="w-5 h-5" /> :
                       step.status === 'running' ? <Loader2 className="w-5 h-5 animate-spin" /> :
                       <div className="w-2 h-2 rounded-full bg-current" />}
                    </div>
                    <span className={`text-sm font-medium ${
                        step.status === 'pending' ? 'text-google-gray-400' : 'text-google-gray-700'
                    }`}>
                      {step.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Output & Logs */}
          <div className="lg:col-span-8 space-y-6">
            
            {/* Live Terminal */}
            <div className="bg-google-gray-900 rounded-2xl p-6 shadow-lg overflow-hidden flex flex-col h-[300px]">
              <div className="flex items-center justify-between mb-4 border-b border-google-gray-700 pb-2">
                <h2 className="text-sm font-medium text-google-gray-300 flex items-center gap-2">
                  <Terminal className="w-4 h-4" />
                  Agent Terminal
                </h2>
                <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-google-red" />
                    <div className="w-2.5 h-2.5 rounded-full bg-google-yellow" />
                    <div className="w-2.5 h-2.5 rounded-full bg-google-green" />
                </div>
              </div>
              <div className="flex-1 overflow-y-auto font-mono text-xs space-y-1.5 pr-2 scrollbar-thin scrollbar-thumb-google-gray-700">
                {logs.length === 0 && (
                    <div className="text-google-gray-500 italic">Ready to start mission...</div>
                )}
                {logs.map((log, i) => (
                  <div key={i} className={`flex gap-3 ${
                    log.type === 'error' ? 'text-google-red' :
                    log.type === 'status' ? 'text-google-blue' :
                    log.type === 'data' ? 'text-google-green' :
                    'text-google-gray-300'
                  }`}>
                    <span className="text-google-gray-600 shrink-0">[{log.timestamp}]</span>
                    <span>
                        {typeof log.content === 'string' ? log.content : JSON.stringify(log.content)}
                    </span>
                  </div>
                ))}
                <div ref={logsEndRef} />
              </div>
            </div>

            {/* Markdown Editor */}
            <div className="bg-white rounded-2xl border border-google-gray-200 shadow-sm overflow-hidden min-h-[500px] flex flex-col">
                 <div className="p-4 border-b border-google-gray-200 bg-google-gray-50 flex items-center justify-between">
                    <h2 className="text-lg font-normal text-google-gray-900 flex items-center gap-2">
                        <FileText className="w-5 h-5 text-google-gray-500" />
                        Content Briefing
                    </h2>
                    {briefing && (
                        <span className="text-xs font-medium px-2 py-1 bg-google-green/10 text-google-green rounded-full">
                            Generated
                        </span>
                    )}
                 </div>
                 <div className="flex-1" data-color-mode="light">
                    <MDEditor
                        value={briefing}
                        onChange={(val) => setBriefing(val || '')}
                        height="100%"
                        preview="live"
                        className="border-none"
                        visibleDragbar={false}
                    />
                 </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
