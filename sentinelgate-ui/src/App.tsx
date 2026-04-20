
// import { useMemo, useState } from "react";
// import "./App.css";

// type ScanResponse = {
//   decision: "PASSED" | "BLOCKED";
//   layer_caught: "L0" | "L1" | "L2" | "UNKNOWN";
//   reason: string;
//   gate_latency_ms: number;
//   action: "SEND_TO_LLM" | "REJECT_REQUEST";
//   original_prompt?: string;
//   clean_prompt?: string;
//   debug?: {
//     similarity?: number | null;
//     margin?: number | null;
//   };
// };

// type HistoryItem = {
//   id: string;
//   ts: string;
//   prompt: string;
//   result: ScanResponse;
// };

// function nowLabel() {
//   return new Date().toLocaleString();
// }
// function uid() {
//   return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
// }

// async function copyToClipboard(text: string) {
//   if (navigator.clipboard?.writeText) {
//     await navigator.clipboard.writeText(text);
//     return;
//   }
//   const ta = document.createElement("textarea");
//   ta.value = text;
//   document.body.appendChild(ta);
//   ta.select();
//   document.execCommand("copy");
//   document.body.removeChild(ta);
// }

// export default function App() {
//   const [prompt, setPrompt] = useState("");
//   const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
//   const [history, setHistory] = useState<HistoryItem[]>([]);
//   const [isScanning, setIsScanning] = useState(false);
//   const [toast, setToast] = useState<string | null>(null);

//   const latestJson = useMemo(() => {
//     return scanResult ? JSON.stringify(scanResult, null, 2) : "";
//   }, [scanResult]);

//   function showToast(msg: string) {
//     setToast(msg);
//     window.setTimeout(() => setToast(null), 1600);
//   }

//   async function scanOnce(p: string) {
//     const res = await fetch("/scan", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ prompt: p }),
//     });

//     if (!res.ok) {
//       const err = await res.json().catch(() => ({}));
//       throw new Error(err?.detail || `Scan failed (${res.status})`);
//     }
//     return (await res.json()) as ScanResponse;
//   }

//   async function onScan() {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       const data = await scanOnce(p);
//       setScanResult(data);
//       setHistory((prev) => {
//         const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//         return [item, ...prev].slice(0, 10);
//       });
//     } catch (e: any) {
//       showToast(e?.message || "Scan error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onRunNx(n: number) {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       for (let i = 0; i < n; i++) {
//         const data = await scanOnce(p);
//         setScanResult(data);
//         setHistory((prev) => {
//           const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//           return [item, ...prev].slice(0, 10);
//         });
//       }
//       showToast(`Ran ${n} scans`);
//     } catch (e: any) {
//       showToast(e?.message || "Run error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onCopyJson() {
//     if (!scanResult) return showToast("No scan result to copy");
//     await copyToClipboard(latestJson);
//     showToast("Copied JSON");
//   }

//   function pillClass() {
//     if (!scanResult) return "pill";
//     return scanResult.decision === "PASSED" ? "pill pill-pass" : "pill pill-block";
//   }

//   function onLoadFromHistory(item: HistoryItem) {
//     setPrompt(item.prompt);
//     setScanResult(item.result);
//     showToast("Loaded from history");
//   }

//   return (
//     <div className="bg">
//       <div className="shell">
//         <header className="top">
//           <div>
//             <div className="brand">
//               <div className="logo">SG</div>
//               <div>
//                 <h1>SentinelGate</h1>
//                 <p>Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.</p>
//               </div>
//             </div>
//           </div>

//           <div className="rightStats">
//             <div className="kpi">
//               <div className="kpiLabel">Status</div>
//               <div className="kpiValue">{scanResult ? scanResult.decision : "—"}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Layer</div>
//               <div className="kpiValue">{scanResult ? scanResult.layer_caught : "—"}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Latency</div>
//               <div className="kpiValue">{scanResult ? `${scanResult.gate_latency_ms} ms` : "—"}</div>
//             </div>
//           </div>
//         </header>

//         {toast && <div className="toast">{toast}</div>}

//         <section className="card inputCard">
//           <div className="fieldRow">
//             <div className="field">
//               <label>Prompt</label>
//               <input
//                 value={prompt}
//                 onChange={(e) => setPrompt(e.target.value)}
//                 placeholder='Try: "shipment tracking status for order 8842 from carrier"'
//               />
//               <div className="hint">
//                 Tip: Try junk (“hi”), noise (“tell me a joke”), domain (“shipment delay status”), and off-domain (“reset my password”).
//               </div>
//             </div>

//             <div className="btnCol">
//               <button className="btn primary" onClick={onScan} disabled={isScanning}>
//                 {isScanning ? "Scanning…" : "Scan"}
//               </button>
//               <button className="btn" onClick={() => onRunNx(10)} disabled={isScanning}>
//                 Run 10×
//               </button>
//               <button className="btn" onClick={onCopyJson} disabled={!scanResult}>
//                 Copy JSON
//               </button>
//               <button className="btn danger" onClick={() => setHistory([])} disabled={history.length === 0}>
//                 Clear History
//               </button>
//             </div>
//           </div>
//         </section>

//         <main className="grid">
//           <section className="card">
//             <div className="cardHead">
//               <h2>Scan Result</h2>
//               <div className={pillClass()}>
//                 {scanResult ? `${scanResult.decision} • ${scanResult.layer_caught}` : "No result"}
//               </div>
//             </div>

//             {!scanResult ? (
//               <div className="empty">
//                 Run a scan to see the decision, reasoning, and debug metrics.
//               </div>
//             ) : (
//               <>
//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Reason</div>
//                     <div className="metricValue">{scanResult.reason}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Action</div>
//                     <div className="metricValue">{scanResult.action}</div>
//                   </div>
//                 </div>

//                 <div className="split">
//                   <div className="box">
//                     <div className="boxLabel">Original</div>
//                     <div className="mono">{scanResult.original_prompt ?? "(not returned)"}</div>
//                   </div>
//                   <div className="box">
//                     <div className="boxLabel">Sanitized</div>
//                     <div className="mono">{scanResult.clean_prompt ?? "(not returned)"}</div>
//                   </div>
//                 </div>

//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Similarity</div>
//                     <div className="metricValue">{scanResult.debug?.similarity ?? "n/a"}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Margin</div>
//                     <div className="metricValue">{scanResult.debug?.margin ?? "n/a"}</div>
//                   </div>
//                 </div>

//                 <div className="codeBlock">
//                   <div className="codeHead">
//                     <div>Raw JSON</div>
//                     <button className="miniBtn" onClick={onCopyJson}>Copy</button>
//                   </div>
//                   <pre>{latestJson}</pre>
//                 </div>
//               </>
//             )}
//           </section>

//           <section className="card">
//             <div className="cardHead">
//               <h2>History</h2>
//               <div className="subtle">Last 10 scans</div>
//             </div>

//             {history.length === 0 ? (
//               <div className="empty">No scans yet.</div>
//             ) : (
//               <div className="historyList">
//                 {history.map((h) => {
//                   const badge = h.result.decision === "PASSED" ? "hBadge pass" : "hBadge block";
//                   return (
//                     <button key={h.id} className="historyItem" onClick={() => onLoadFromHistory(h)}>
//                       <div className="historyTop">
//                         <div className={badge}>{h.result.decision}</div>
//                         <div className="historyMeta">{h.ts}</div>
//                       </div>
//                       <div className="historyPrompt">{h.prompt}</div>
//                       <div className="historyFoot">
//                         <span>layer: {h.result.layer_caught}</span>
//                         <span>reason: {h.result.reason}</span>
//                         <span>{h.result.gate_latency_ms} ms</span>
//                       </div>
//                     </button>
//                   );
//                 })}
//               </div>
//             )}
//           </section>
//         </main>

//         <footer className="foot">
//           <span>SentinelGate • Supply Chain domain config • tau = 0.10</span>
//         </footer>
//       </div>
//     </div>
//   );
// }




// import { useMemo, useState } from "react";
// import "./App.css";

// type ApprovedMatch = {
//   id: string;
//   domain: string;
//   text: string;
//   similarity: number;
// };

// type ScanResponse = {
//   decision: "PASSED" | "BLOCKED";
//   layer_caught: "L0" | "L1" | "L2" | "L2.5" | "UNKNOWN";
//   reason: string;
//   gate_latency_ms: number;
//   action: "SEND_TO_LLM" | "REJECT_REQUEST";
//   original_prompt?: string;
//   clean_prompt?: string;
//   approved_match?: ApprovedMatch | null;
//   debug?: {
//     similarity?: number | null;
//     margin?: number | null;
//   };
// };

// type HistoryItem = {
//   id: string;
//   ts: string;
//   prompt: string;
//   result: ScanResponse;
// };

// function nowLabel() {
//   return new Date().toLocaleString();
// }
// function uid() {
//   return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
// }

// async function copyToClipboard(text: string) {
//   if (navigator.clipboard?.writeText) {
//     await navigator.clipboard.writeText(text);
//     return;
//   }
//   const ta = document.createElement("textarea");
//   ta.value = text;
//   document.body.appendChild(ta);
//   ta.select();
//   document.execCommand("copy");
//   document.body.removeChild(ta);
// }

// export default function App() {
//   const [prompt, setPrompt] = useState("");
//   const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
//   const [history, setHistory] = useState<HistoryItem[]>([]);
//   const [isScanning, setIsScanning] = useState(false);
//   const [toast, setToast] = useState<string | null>(null);

//   const latestJson = useMemo(() => {
//     return scanResult ? JSON.stringify(scanResult, null, 2) : "";
//   }, [scanResult]);

//   function showToast(msg: string) {
//     setToast(msg);
//     window.setTimeout(() => setToast(null), 1600);
//   }

//   async function scanOnce(p: string) {
//     const res = await fetch("/scan", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ prompt: p }),
//     });

//     if (!res.ok) {
//       const err = await res.json().catch(() => ({}));
//       throw new Error(err?.detail || `Scan failed (${res.status})`);
//     }
//     return (await res.json()) as ScanResponse;
//   }

//   async function onScan() {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       const data = await scanOnce(p);
//       setScanResult(data);
//       setHistory((prev) => {
//         const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//         return [item, ...prev].slice(0, 10);
//       });
//     } catch (e: any) {
//       showToast(e?.message || "Scan error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onRunNx(n: number) {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       for (let i = 0; i < n; i++) {
//         const data = await scanOnce(p);
//         setScanResult(data);
//         setHistory((prev) => {
//           const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//           return [item, ...prev].slice(0, 10);
//         });
//       }
//       showToast(`Ran ${n} scans`);
//     } catch (e: any) {
//       showToast(e?.message || "Run error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onCopyJson() {
//     if (!scanResult) return showToast("No scan result to copy");
//     await copyToClipboard(latestJson);
//     showToast("Copied JSON");
//   }

//   function pillClass() {
//     if (!scanResult) return "pill";
//     return scanResult.decision === "PASSED" ? "pill pill-pass" : "pill pill-block";
//   }

//   function onLoadFromHistory(item: HistoryItem) {
//     setPrompt(item.prompt);
//     setScanResult(item.result);
//     showToast("Loaded from history");
//   }

//   const kpiDecision = scanResult ? scanResult.decision : "—";
//   const kpiLayer = scanResult ? scanResult.layer_caught : "—";
//   const kpiLatency = scanResult ? `${scanResult.gate_latency_ms} ms` : "—";

//   return (
//     <div className="bg">
//       <div className="shell">
//         <header className="top">
//           <div className="brand">
//             <div className="logo">SG</div>
//             <div>
//               <h1>SentinelGate</h1>
//               <p>Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.</p>
//             </div>
//           </div>

//           <div className="rightStats">
//             <div className="kpi">
//               <div className="kpiLabel">Status</div>
//               <div className="kpiValue">{kpiDecision}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Layer</div>
//               <div className="kpiValue">{kpiLayer}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Latency</div>
//               <div className="kpiValue">{kpiLatency}</div>
//             </div>
//           </div>
//         </header>

//         {toast && <div className="toast">{toast}</div>}

//         <section className="card inputCard">
//           <div className="fieldRow">
//             <div className="field">
//               <label>Prompt</label>
//               <input
//                 value={prompt}
//                 onChange={(e) => setPrompt(e.target.value)}
//                 placeholder='Try: "shipment tracking status for order 8842 from carrier"'
//               />
//               <div className="hint">
//                 Try: junk (“hi”), noise (“tell me a joke”), domain (“shipment delay status”), off-domain (“reset my password”), or bypass memory (“vpn not working on corporate laptop”).
//               </div>
//             </div>

//             <div className="btnCol">
//               <button className="btn primary" onClick={onScan} disabled={isScanning}>
//                 {isScanning ? "Scanning…" : "Scan"}
//               </button>
//               <button className="btn" onClick={() => onRunNx(10)} disabled={isScanning}>
//                 Run 10×
//               </button>
//               <button className="btn" onClick={onCopyJson} disabled={!scanResult}>
//                 Copy JSON
//               </button>
//               <button className="btn danger" onClick={() => setHistory([])} disabled={history.length === 0}>
//                 Clear History
//               </button>
//             </div>
//           </div>
//         </section>

//         <main className="grid">
//           <section className="card">
//             <div className="cardHead">
//               <h2>Scan Result</h2>
//               <div className={pillClass()}>
//                 {scanResult ? `${scanResult.decision} • ${scanResult.layer_caught}` : "No result"}
//               </div>
//             </div>

//             {!scanResult ? (
//               <div className="empty">Run a scan to see the decision, reasoning, and debug metrics.</div>
//             ) : (
//               <>
//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Reason</div>
//                     <div className="metricValue">{scanResult.reason}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Action</div>
//                     <div className="metricValue">{scanResult.action}</div>
//                   </div>
//                 </div>

//                 {scanResult.reason === "approved_match" && scanResult.approved_match ? (
//                   <div className="box" style={{ marginBottom: 12 }}>
//                     <div className="boxLabel">Approved Match (L2.5)</div>
//                     <div className="mono">
//                       domain: {scanResult.approved_match.domain}
//                       {"\n"}similarity: {scanResult.approved_match.similarity}
//                       {"\n"}text: {scanResult.approved_match.text}
//                     </div>
//                   </div>
//                 ) : null}

//                 <div className="split">
//                   <div className="box">
//                     <div className="boxLabel">Original</div>
//                     <div className="mono">{scanResult.original_prompt ?? "(not returned)"}</div>
//                   </div>
//                   <div className="box">
//                     <div className="boxLabel">Sanitized</div>
//                     <div className="mono">{scanResult.clean_prompt ?? "(not returned)"}</div>
//                   </div>
//                 </div>

//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Similarity</div>
//                     <div className="metricValue">{scanResult.debug?.similarity ?? scanResult.debug?.similarity === 0 ? 0 : "n/a"}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Margin</div>
//                     <div className="metricValue">{scanResult.debug?.margin ?? scanResult.debug?.margin === 0 ? 0 : "n/a"}</div>
//                   </div>
//                 </div>

//                 <div className="codeBlock">
//                   <div className="codeHead">
//                     <div>Raw JSON</div>
//                     <button className="miniBtn" onClick={onCopyJson}>Copy</button>
//                   </div>
//                   <pre>{latestJson}</pre>
//                 </div>
//               </>
//             )}
//           </section>

//           <section className="card">
//             <div className="cardHead">
//               <h2>History</h2>
//               <div className="subtle">Last 10 scans</div>
//             </div>

//             {history.length === 0 ? (
//               <div className="empty">No scans yet.</div>
//             ) : (
//               <div className="historyList">
//                 {history.map((h) => {
//                   const badge = h.result.decision === "PASSED" ? "hBadge pass" : "hBadge block";
//                   return (
//                     <button key={h.id} className="historyItem" onClick={() => onLoadFromHistory(h)}>
//                       <div className="historyTop">
//                         <div className={badge}>{h.result.decision}</div>
//                         <div className="historyMeta">{h.ts}</div>
//                       </div>
//                       <div className="historyPrompt">{h.prompt}</div>
//                       <div className="historyFoot">
//                         <span>layer: {h.result.layer_caught}</span>
//                         <span>reason: {h.result.reason}</span>
//                         <span>{h.result.gate_latency_ms} ms</span>
//                       </div>
//                     </button>
//                   );
//                 })}
//               </div>
//             )}
//           </section>
//         </main>

//         <footer className="foot">
//           <span>SentinelGate • Supply Chain + Approved Bypass Memory • tau = 0.10</span>
//         </footer>
//       </div>
//     </div>
//   );
// }


// import { useMemo, useState } from "react";
// import "./App.css";

// type ApprovedMatch = {
//   id: string;
//   domain: string;
//   text: string;
//   similarity: number;
// };

// type ScanResponse = {
//   decision: "PASSED" | "BLOCKED";
//   layer_caught: "L0" | "L1" | "L2" | "L2.5" | "UNKNOWN";
//   reason: string;
//   gate_latency_ms: number;
//   action: "SEND_TO_LLM" | "REJECT_REQUEST";
//   original_prompt?: string;
//   clean_prompt?: string;
//   approved_match?: ApprovedMatch | null;
//   debug?: {
//     similarity?: number | null;
//     margin?: number | null;
//   };
// };

// type HistoryItem = {
//   id: string;
//   ts: string;
//   prompt: string;
//   result: ScanResponse;
// };

// function nowLabel() {
//   return new Date().toLocaleString();
// }
// function uid() {
//   return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
// }

// async function copyToClipboard(text: string) {
//   if (navigator.clipboard?.writeText) {
//     await navigator.clipboard.writeText(text);
//     return;
//   }
//   const ta = document.createElement("textarea");
//   ta.value = text;
//   document.body.appendChild(ta);
//   ta.select();
//   document.execCommand("copy");
//   document.body.removeChild(ta);
// }

// export default function App() {
//   const [prompt, setPrompt] = useState("");
//   const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
//   const [history, setHistory] = useState<HistoryItem[]>([]);
//   const [isScanning, setIsScanning] = useState(false);
//   const [toast, setToast] = useState<string | null>(null);

//   const latestJson = useMemo(() => {
//     return scanResult ? JSON.stringify(scanResult, null, 2) : "";
//   }, [scanResult]);

//   function showToast(msg: string) {
//     setToast(msg);
//     window.setTimeout(() => setToast(null), 1600);
//   }

//   async function scanOnce(p: string) {
//     const res = await fetch("/scan", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ prompt: p }),
//     });

//     if (!res.ok) {
//       const err = await res.json().catch(() => ({}));
//       throw new Error(err?.detail || `Scan failed (${res.status})`);
//     }
//     return (await res.json()) as ScanResponse;
//   }

//   async function onScan() {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       const data = await scanOnce(p);
//       setScanResult(data);
//       setHistory((prev) => {
//         const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//         return [item, ...prev].slice(0, 10);
//       });
//     } catch (e: any) {
//       showToast(e?.message || "Scan error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onRunNx(n: number) {
//     const p = prompt;
//     if (!p.trim()) return showToast("Enter a prompt first");

//     setIsScanning(true);
//     try {
//       for (let i = 0; i < n; i++) {
//         const data = await scanOnce(p);
//         setScanResult(data);
//         setHistory((prev) => {
//           const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
//           return [item, ...prev].slice(0, 10);
//         });
//       }
//       showToast(`Ran ${n} scans`);
//     } catch (e: any) {
//       showToast(e?.message || "Run error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onCopyJson() {
//     if (!scanResult) return showToast("No scan result to copy");
//     await copyToClipboard(latestJson);
//     showToast("Copied JSON");
//   }

//   function pillClass() {
//     if (!scanResult) return "pill";
//     return scanResult.decision === "PASSED" ? "pill pill-pass" : "pill pill-block";
//   }

//   function onLoadFromHistory(item: HistoryItem) {
//     setPrompt(item.prompt);
//     setScanResult(item.result);
//     showToast("Loaded from history");
//   }

//   const kpiDecision = scanResult ? scanResult.decision : "—";
//   const kpiLayer = scanResult ? scanResult.layer_caught : "—";
//   const kpiLatency = scanResult ? `${scanResult.gate_latency_ms} ms` : "—";

//   const sim =
//     typeof scanResult?.debug?.similarity === "number" ? scanResult.debug.similarity : null;

//   const margin =
//     typeof scanResult?.debug?.margin === "number" ? scanResult.debug.margin : null;

//   return (
//     <div className="bg">
//       <div className="shell">
//         <header className="top">
//           <div className="brand">
//             <div className="logo">SG</div>
//             <div>
//               <h1>SentinelGate</h1>
//               <p>Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.</p>
//             </div>
//           </div>

//           <div className="rightStats">
//             <div className="kpi">
//               <div className="kpiLabel">Status</div>
//               <div className="kpiValue">{kpiDecision}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Layer</div>
//               <div className="kpiValue">{kpiLayer}</div>
//             </div>
//             <div className="kpi">
//               <div className="kpiLabel">Latency</div>
//               <div className="kpiValue">{kpiLatency}</div>
//             </div>
//           </div>
//         </header>

//         {toast && <div className="toast">{toast}</div>}

//         <section className="card inputCard">
//           <div className="fieldRow">
//             <div className="field">
//               <label>Prompt</label>
//               <input
//                 value={prompt}
//                 onChange={(e) => setPrompt(e.target.value)}
//                 placeholder='Try: "shipment tracking status for order 8842 from carrier"'
//               />
//               <div className="hint">
//                 Try: junk (“hi”), noise (“tell me a joke”), domain (“shipment delay status”), off-domain (“reset my password”), or bypass memory (“vpn not working on corporate laptop”).
//               </div>
//             </div>

//             <div className="btnCol">
//               <button className="btn primary" onClick={onScan} disabled={isScanning}>
//                 {isScanning ? "Scanning…" : "Scan"}
//               </button>
//               <button className="btn" onClick={() => onRunNx(10)} disabled={isScanning}>
//                 Run 10×
//               </button>
//               <button className="btn" onClick={onCopyJson} disabled={!scanResult}>
//                 Copy JSON
//               </button>
//               <button className="btn danger" onClick={() => setHistory([])} disabled={history.length === 0}>
//                 Clear History
//               </button>
//             </div>
//           </div>
//         </section>

//         <main className="grid">
//           <section className="card">
//             <div className="cardHead">
//               <h2>Scan Result</h2>
//               <div className={pillClass()}>
//                 {scanResult ? `${scanResult.decision} • ${scanResult.layer_caught}` : "No result"}
//               </div>
//             </div>

//             {!scanResult ? (
//               <div className="empty">Run a scan to see the decision, reasoning, and debug metrics.</div>
//             ) : (
//               <>
//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Reason</div>
//                     <div className="metricValue">{scanResult.reason}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Action</div>
//                     <div className="metricValue">{scanResult.action}</div>
//                   </div>
//                 </div>

//                 {scanResult.reason === "approved_match" && scanResult.approved_match ? (
//                   <div className="box" style={{ marginBottom: 12 }}>
//                     <div className="boxLabel">Approved Match (L2.5)</div>
//                     <div className="mono">
//                       domain: {scanResult.approved_match.domain}
//                       {"\n"}similarity: {scanResult.approved_match.similarity.toFixed(4)}
//                       {"\n"}text: {scanResult.approved_match.text}
//                     </div>
//                   </div>
//                 ) : null}

//                 <div className="split">
//                   <div className="box">
//                     <div className="boxLabel">Original</div>
//                     <div className="mono">{scanResult.original_prompt ?? "(not returned)"}</div>
//                   </div>
//                   <div className="box">
//                     <div className="boxLabel">Sanitized</div>
//                     <div className="mono">{scanResult.clean_prompt ?? "(not returned)"}</div>
//                   </div>
//                 </div>

//                 <div className="row">
//                   <div className="metric">
//                     <div className="metricLabel">Similarity</div>
//                     <div className="metricValue">{sim !== null ? sim.toFixed(4) : "n/a"}</div>
//                   </div>
//                   <div className="metric">
//                     <div className="metricLabel">Margin</div>
//                     <div className="metricValue">{margin !== null ? margin.toFixed(4) : "n/a"}</div>
//                   </div>
//                 </div>

//                 <div className="codeBlock">
//                   <div className="codeHead">
//                     <div>Raw JSON</div>
//                     <button className="miniBtn" onClick={onCopyJson}>Copy</button>
//                   </div>
//                   <pre>{latestJson}</pre>
//                 </div>
//               </>
//             )}
//           </section>

//           <section className="card">
//             <div className="cardHead">
//               <h2>History</h2>
//               <div className="subtle">Last 10 scans</div>
//             </div>

//             {history.length === 0 ? (
//               <div className="empty">No scans yet.</div>
//             ) : (
//               <div className="historyList">
//                 {history.map((h) => {
//                   const badge = h.result.decision === "PASSED" ? "hBadge pass" : "hBadge block";
//                   return (
//                     <button key={h.id} className="historyItem" onClick={() => onLoadFromHistory(h)}>
//                       <div className="historyTop">
//                         <div className={badge}>{h.result.decision}</div>
//                         <div className="historyMeta">{h.ts}</div>
//                       </div>
//                       <div className="historyPrompt">{h.prompt}</div>
//                       <div className="historyFoot">
//                         <span>layer: {h.result.layer_caught}</span>
//                         <span>reason: {h.result.reason}</span>
//                         <span>{h.result.gate_latency_ms} ms</span>
//                       </div>
//                     </button>
//                   );
//                 })}
//               </div>
//             )}
//           </section>
//         </main>

//         <footer className="foot">
//           <span>SentinelGate • Supply Chain + Approved Bypass Memory • tau = 0.10</span>
//         </footer>
//       </div>
//     </div>
//   );
// }



import { useMemo, useState } from "react";
import "./App.css";

type ApprovedMatch = {
  id: string;
  domain: string;
  text: string;
  similarity: number;
};

type ScanResponse = {
  decision: "PASSED" | "BLOCKED";
  layer_caught: "L0" | "L1" | "L2" | "L2.5" | "UNKNOWN";
  reason: string;
  gate_latency_ms: number;
  action: "SEND_TO_LLM" | "REJECT_REQUEST";
  original_prompt?: string;
  clean_prompt?: string;
  approved_match?: ApprovedMatch | null;
  debug?: {
    similarity?: number | null;
    margin?: number | null;
  };
};

type HistoryItem = {
  id: string;
  ts: string;
  prompt: string;
  result: ScanResponse;
};

type AnalyticsResponse = {
  report: string;
  metrics: {
    total_requests: number;
    prompts_blocked: number;
    prompts_passed: number;
    efficiency_rate: string;
  };
  financial_impact: {
    estimated_usd_saved: string;
    tokens_prevented: number;
  };
  performance_impact: {
    total_latency_saved_seconds: number;
    avg_gate_latency_ms: string;
  };
};

type BypassRequestIn = {
  prompt: string;
  requested_domain: string;
  user_reason: string;
};

type BypassRequestOut = {
  status: "ok";
  request_id: string;
  clean_prompt: string;
};

type BypassRequestItem = {
  id: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  requested_domain: string;
  user_reason: string;
  original_prompt: string;
  clean_prompt: string;
  created_at: string;
  reviewed_at?: string | null;
  reviewed_by?: string | null;
  review_note?: string | null;
};

type BypassRequestsOut = {
  items: BypassRequestItem[];
};

type ApproveRequestIn = {
  request_id: string;
  approved_by: string;
  canonical_text?: string;
  domain?: string;
};

function nowLabel() {
  return new Date().toLocaleString();
}
function uid() {
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

async function copyToClipboard(text: string) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const ta = document.createElement("textarea");
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  document.body.removeChild(ta);
}

function fmtIso(iso?: string | null) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [isLoadingAnalytics, setIsLoadingAnalytics] = useState(false);

  // Bypass request (user side)
  const [requestedDomain, setRequestedDomain] = useState("it_helpdesk");
  const [userReason, setUserReason] = useState("Need to route this to the right assistant");
  const [bypassReqId, setBypassReqId] = useState<string | null>(null);
  const [bypassReqOut, setBypassReqOut] = useState<BypassRequestOut | null>(null);

  // Admin panel
  const [adminKey, setAdminKey] = useState("");
  const [adminApprovedBy, setAdminApprovedBy] = useState("admin@company.com");
  const [adminCanonicalText, setAdminCanonicalText] = useState("");
  const [adminDomain, setAdminDomain] = useState("");
  const [adminRequests, setAdminRequests] = useState<BypassRequestItem[]>([]);
  const [isLoadingAdmin, setIsLoadingAdmin] = useState(false);
  const [isApproving, setIsApproving] = useState(false);
  const [selectedRequestId, setSelectedRequestId] = useState<string>("");

  const latestJson = useMemo(() => {
    return scanResult ? JSON.stringify(scanResult, null, 2) : "";
  }, [scanResult]);

  function showToast(msg: string) {
    setToast(msg);
    window.setTimeout(() => setToast(null), 1800);
  }

  async function scanOnce(p: string) {
    const res = await fetch("/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: p }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err?.detail || `Scan failed (${res.status})`);
    }
    return (await res.json()) as ScanResponse;
  }

  async function onScan() {
    const p = prompt;
    if (!p.trim()) return showToast("Enter a prompt first");

    setIsScanning(true);
    try {
      const data = await scanOnce(p);
      setScanResult(data);
      setHistory((prev) => {
        const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
        return [item, ...prev].slice(0, 10);
      });
    } catch (e: any) {
      showToast(e?.message || "Scan error");
    } finally {
      setIsScanning(false);
    }
  }

  async function onRunNx(n: number) {
    const p = prompt;
    if (!p.trim()) return showToast("Enter a prompt first");

    setIsScanning(true);
    try {
      for (let i = 0; i < n; i++) {
        const data = await scanOnce(p);
        setScanResult(data);
        setHistory((prev) => {
          const item: HistoryItem = { id: uid(), ts: nowLabel(), prompt: p, result: data };
          return [item, ...prev].slice(0, 10);
        });
      }
      showToast(`Ran ${n} scans`);
    } catch (e: any) {
      showToast(e?.message || "Run error");
    } finally {
      setIsScanning(false);
    }
  }

  async function onCopyJson() {
    if (!scanResult) return showToast("No scan result to copy");
    await copyToClipboard(latestJson);
    showToast("Copied JSON");
  }

  function pillClass() {
    if (!scanResult) return "pill";
    return scanResult.decision === "PASSED" ? "pill pill-pass" : "pill pill-block";
  }

  function onLoadFromHistory(item: HistoryItem) {
    setPrompt(item.prompt);
    setScanResult(item.result);
    showToast("Loaded from history");
  }

  const kpiDecision = scanResult ? scanResult.decision : "—";
  const kpiLayer = scanResult ? scanResult.layer_caught : "—";
  const kpiLatency = scanResult ? `${scanResult.gate_latency_ms} ms` : "—";

  const sim = typeof scanResult?.debug?.similarity === "number" ? scanResult.debug.similarity : null;
  const margin = typeof scanResult?.debug?.margin === "number" ? scanResult.debug.margin : null;

  async function onLoadAnalytics() {
    setIsLoadingAnalytics(true);
    try {
      const res = await fetch("/analytics");
      if (!res.ok) throw new Error(`Analytics failed (${res.status})`);
      const data = (await res.json()) as AnalyticsResponse;
      setAnalytics(data);
      showToast("Analytics loaded");
    } catch (e: any) {
      showToast(e?.message || "Analytics error");
    } finally {
      setIsLoadingAnalytics(false);
    }
  }

  async function onBypassRequest() {
    const p = prompt;
    if (!p.trim()) return showToast("Enter a prompt first (use an off-domain prompt)");
    if (!requestedDomain.trim()) return showToast("Requested domain required");
    if (!userReason.trim()) return showToast("Reason required");

    const body: BypassRequestIn = {
      prompt: p,
      requested_domain: requestedDomain.trim(),
      user_reason: userReason.trim(),
    };

    try {
      const res = await fetch("/bypass/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err?.detail || `Bypass request failed (${res.status})`);
      }
      const out = (await res.json()) as BypassRequestOut;
      setBypassReqId(out.request_id);
      setBypassReqOut(out);
      showToast("Bypass request created");
    } catch (e: any) {
      showToast(e?.message || "Bypass request error");
    }
  }

  async function onAdminLoadPending() {
    setIsLoadingAdmin(true);
    try {
      const res = await fetch("/admin/bypass/requests?status=PENDING", {
        headers: adminKey ? { "X-Admin-Key": adminKey } : undefined,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err?.detail || `Load requests failed (${res.status})`);
      }
      const out = (await res.json()) as BypassRequestsOut;
      setAdminRequests(out.items || []);
      showToast(`Loaded ${out.items?.length ?? 0} pending request(s)`);
    } catch (e: any) {
      showToast(e?.message || "Admin load error");
    } finally {
      setIsLoadingAdmin(false);
    }
  }

  async function onAdminApprove() {
    if (!selectedRequestId) return showToast("Select a request first");
    if (!adminApprovedBy.trim()) return showToast("approved_by required");

    setIsApproving(true);
    try {
      const body: ApproveRequestIn = {
        request_id: selectedRequestId,
        approved_by: adminApprovedBy.trim(),
        canonical_text: adminCanonicalText.trim() ? adminCanonicalText.trim() : undefined,
        domain: adminDomain.trim() ? adminDomain.trim() : undefined,
      };

      const res = await fetch("/admin/bypass/approve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(adminKey ? { "X-Admin-Key": adminKey } : {}),
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err?.detail || `Approve failed (${res.status})`);
      }

      await res.json();
      showToast("Approved + stored to memory (L2.5)");
      setAdminCanonicalText("");
      setAdminDomain("");
      await onAdminLoadPending();
    } catch (e: any) {
      showToast(e?.message || "Approve error");
    } finally {
      setIsApproving(false);
    }
  }

  function pickRequest(id: string) {
    setSelectedRequestId(id);
    const req = adminRequests.find((r) => r.id === id);
    if (req) {
      // helpful defaults
      if (!adminDomain) setAdminDomain(req.requested_domain);
      if (!adminCanonicalText) setAdminCanonicalText(req.clean_prompt);
    }
  }

  return (
    <div className="bg">
      <div className="shell">
        <header className="top">
          <div className="brand">
            <div className="logo">SG</div>
            <div>
              <h1>SentinelGate</h1>
              <p>Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.</p>
            </div>
          </div>

          <div className="rightStats">
            <div className="kpi">
              <div className="kpiLabel">Status</div>
              <div className="kpiValue">{kpiDecision}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Layer</div>
              <div className="kpiValue">{kpiLayer}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Latency</div>
              <div className="kpiValue">{kpiLatency}</div>
            </div>
          </div>
        </header>

        {toast && <div className="toast">{toast}</div>}

        <section className="card inputCard">
          <div className="fieldRow">
            <div className="field">
              <label>Prompt</label>
              <input
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder='Try: "shipment tracking status for order 8842 from carrier"'
              />
              <div className="hint">
                Try: junk (“hi”), noise (“tell me a joke”), domain (“shipment delay status”), off-domain (“reset my password”), or bypass memory (“vpn not working on corporate laptop”).
              </div>
            </div>

            <div className="btnCol">
              <button className="btn primary" onClick={onScan} disabled={isScanning}>
                {isScanning ? "Scanning…" : "Scan"}
              </button>
              <button className="btn" onClick={() => onRunNx(10)} disabled={isScanning}>
                Run 10×
              </button>
              <button className="btn" onClick={onCopyJson} disabled={!scanResult}>
                Copy JSON
              </button>
              <button className="btn" onClick={onLoadAnalytics} disabled={isLoadingAnalytics}>
                {isLoadingAnalytics ? "Loading…" : "Load Analytics"}
              </button>
              <button className="btn danger" onClick={() => setHistory([])} disabled={history.length === 0}>
                Clear History
              </button>
            </div>
          </div>
        </section>

        <main className="grid">
          <section className="card">
            <div className="cardHead">
              <h2>Scan Result</h2>
              <div className={pillClass()}>
                {scanResult ? `${scanResult.decision} • ${scanResult.layer_caught}` : "No result"}
              </div>
            </div>

            {!scanResult ? (
              <div className="empty">Run a scan to see the decision, reasoning, and debug metrics.</div>
            ) : (
              <>
                <div className="row">
                  <div className="metric">
                    <div className="metricLabel">Reason</div>
                    <div className="metricValue">{scanResult.reason}</div>
                  </div>
                  <div className="metric">
                    <div className="metricLabel">Action</div>
                    <div className="metricValue">{scanResult.action}</div>
                  </div>
                </div>

                {scanResult.reason === "approved_match" && scanResult.approved_match ? (
                  <div className="box" style={{ marginBottom: 12 }}>
                    <div className="boxLabel">Approved Match (L2.5)</div>
                    <div className="mono">
                      domain: {scanResult.approved_match.domain}
                      {"\n"}similarity: {scanResult.approved_match.similarity.toFixed(4)}
                      {"\n"}text: {scanResult.approved_match.text}
                    </div>
                  </div>
                ) : null}

                <div className="split">
                  <div className="box">
                    <div className="boxLabel">Original</div>
                    <div className="mono">{scanResult.original_prompt ?? "(not returned)"}</div>
                  </div>
                  <div className="box">
                    <div className="boxLabel">Sanitized</div>
                    <div className="mono">{scanResult.clean_prompt ?? "(not returned)"}</div>
                  </div>
                </div>

                <div className="row">
                  <div className="metric">
                    <div className="metricLabel">Similarity</div>
                    <div className="metricValue">{sim !== null ? sim.toFixed(4) : "n/a"}</div>
                  </div>
                  <div className="metric">
                    <div className="metricLabel">Margin</div>
                    <div className="metricValue">{margin !== null ? margin.toFixed(4) : "n/a"}</div>
                  </div>
                </div>

                <div className="codeBlock">
                  <div className="codeHead">
                    <div>Raw JSON</div>
                    <button className="miniBtn" onClick={onCopyJson}>Copy</button>
                  </div>
                  <pre>{latestJson}</pre>
                </div>
              </>
            )}
          </section>

          <section className="card">
            <div className="cardHead">
              <h2>History</h2>
              <div className="subtle">Last 10 scans</div>
            </div>

            {history.length === 0 ? (
              <div className="empty">No scans yet.</div>
            ) : (
              <div className="historyList">
                {history.map((h) => {
                  const badge = h.result.decision === "PASSED" ? "hBadge pass" : "hBadge block";
                  return (
                    <button key={h.id} className="historyItem" onClick={() => onLoadFromHistory(h)}>
                      <div className="historyTop">
                        <div className={badge}>{h.result.decision}</div>
                        <div className="historyMeta">{h.ts}</div>
                      </div>
                      <div className="historyPrompt">{h.prompt}</div>
                      <div className="historyFoot">
                        <span>layer: {h.result.layer_caught}</span>
                        <span>reason: {h.result.reason}</span>
                        <span>{h.result.gate_latency_ms} ms</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </section>
        </main>

        {/* ANALYTICS CARD */}
        <section className="card sectionCard">
          <div className="cardHead">
            <h2>Analytics</h2>
            <div className="subtle">Live counters from backend</div>
          </div>

          {!analytics ? (
            <div className="empty">Click “Load Analytics” to fetch the latest FinOps summary.</div>
          ) : (
            <div className="analyticsGrid">
              <div className="metric">
                <div className="metricLabel">Total Requests</div>
                <div className="metricValue">{analytics.metrics.total_requests}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Blocked</div>
                <div className="metricValue">{analytics.metrics.prompts_blocked}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Passed</div>
                <div className="metricValue">{analytics.metrics.prompts_passed}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Efficiency</div>
                <div className="metricValue">{analytics.metrics.efficiency_rate}</div>
              </div>

              <div className="metric">
                <div className="metricLabel">Estimated Saved</div>
                <div className="metricValue">{analytics.financial_impact.estimated_usd_saved}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Tokens Prevented</div>
                <div className="metricValue">{analytics.financial_impact.tokens_prevented}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Latency Saved (s)</div>
                <div className="metricValue">{analytics.performance_impact.total_latency_saved_seconds}</div>
              </div>
              <div className="metric">
                <div className="metricLabel">Gate Latency</div>
                <div className="metricValue">{analytics.performance_impact.avg_gate_latency_ms}</div>
              </div>
            </div>
          )}
        </section>

        {/* BYPASS REQUEST (USER SIDE) */}
        <section className="card sectionCard">
          <div className="cardHead">
            <h2>Bypass Request</h2>
            <div className="subtle">If prompt is off-domain, request expansion with admin approval</div>
          </div>

          <div className="twoCol">
            <div className="field">
              <label>Requested Domain</label>
              <input value={requestedDomain} onChange={(e) => setRequestedDomain(e.target.value)} placeholder="e.g. it_helpdesk" />
            </div>
            <div className="field">
              <label>User Reason</label>
              <input value={userReason} onChange={(e) => setUserReason(e.target.value)} placeholder="Why do you need bypass?" />
            </div>
          </div>

          <div className="btnRow">
            <button className="btn primary" onClick={onBypassRequest} disabled={isScanning}>
              Request Bypass
            </button>
            {bypassReqId ? <div className="tag">request_id: {bypassReqId}</div> : <div className="tag subtleTag">No request yet</div>}
          </div>

          {bypassReqOut ? (
            <div className="codeBlock" style={{ marginTop: 12 }}>
              <div className="codeHead">
                <div>Bypass Request Output</div>
                <button className="miniBtn" onClick={() => copyToClipboard(JSON.stringify(bypassReqOut, null, 2)).then(() => showToast("Copied"))}>
                  Copy
                </button>
              </div>
              <pre>{JSON.stringify(bypassReqOut, null, 2)}</pre>
            </div>
          ) : null}
        </section>

        {/* ADMIN PANEL */}
        <section className="card sectionCard">
          <div className="cardHead">
            <h2>Admin Panel</h2>
            <div className="subtle">Review + approve bypass requests → store as L2.5 memory</div>
          </div>

          <div className="twoCol">
            <div className="field">
              <label>X-Admin-Key</label>
              <input value={adminKey} onChange={(e) => setAdminKey(e.target.value)} placeholder="paste admin key" />
              <div className="hint">This header is required if your backend enforces it.</div>
            </div>

            <div className="field">
              <label>Approved By</label>
              <input value={adminApprovedBy} onChange={(e) => setAdminApprovedBy(e.target.value)} placeholder="admin@company.com" />
            </div>
          </div>

          <div className="btnRow">
            <button className="btn" onClick={onAdminLoadPending} disabled={isLoadingAdmin}>
              {isLoadingAdmin ? "Loading…" : "Load Pending Requests"}
            </button>
            <div className="tag subtleTag">
              pending: {adminRequests.length} • selected: {selectedRequestId ? selectedRequestId.slice(0, 8) + "…" : "—"}
            </div>
          </div>

          {adminRequests.length === 0 ? (
            <div className="empty" style={{ paddingTop: 10 }}>
              No pending requests loaded.
            </div>
          ) : (
            <div className="adminList">
              {adminRequests.map((r) => (
                <button
                  key={r.id}
                  className={`adminItem ${selectedRequestId === r.id ? "adminItemActive" : ""}`}
                  onClick={() => pickRequest(r.id)}
                >
                  <div className="adminTop">
                    <div className="adminBadge">{r.status}</div>
                    <div className="adminMeta">{fmtIso(r.created_at)}</div>
                  </div>
                  <div className="adminPrompt">{r.clean_prompt}</div>
                  <div className="adminFoot">
                    <span>domain: {r.requested_domain}</span>
                    <span>reason: {r.user_reason}</span>
                  </div>
                </button>
              ))}
            </div>
          )}

          <div className="divider" />

          <div className="twoCol">
            <div className="field">
              <label>Domain (optional override)</label>
              <input value={adminDomain} onChange={(e) => setAdminDomain(e.target.value)} placeholder="defaults from request" />
            </div>
            <div className="field">
              <label>Canonical Text (recommended)</label>
              <input
                value={adminCanonicalText}
                onChange={(e) => setAdminCanonicalText(e.target.value)}
                placeholder="Rewrite into a clean canonical example"
              />
            </div>
          </div>

          <div className="btnRow">
            <button className="btn primary" onClick={onAdminApprove} disabled={isApproving}>
              {isApproving ? "Approving…" : "Approve Selected"}
            </button>
            <div className="hint">
              After approval, scan a similar prompt → it should PASS via <b>L2.5 approved_match</b>.
            </div>
          </div>
        </section>

        <footer className="foot">
          <span>SentinelGate • Supply Chain + Approved Bypass Memory • tau = 0.10</span>
        </footer>
      </div>
    </div>
  );
}
