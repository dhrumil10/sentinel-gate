
// import { useMemo, useState } from "react";

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
//     window.setTimeout(() => setToast(null), 1500);
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

//     const data = (await res.json()) as ScanResponse;
//     return data;
//   }

//   async function onScan() {
//     const p = prompt;
//     if (!p.trim()) {
//       showToast("Enter a prompt first");
//       return;
//     }

//     setIsScanning(true);
//     try {
//       const data = await scanOnce(p);
//       setScanResult(data);

//       // add to history (keep last 10)
//       setHistory((prev) => {
//         const item: HistoryItem = {
//           id: uid(),
//           ts: nowLabel(),
//           prompt: p,
//           result: data,
//         };
//         const next = [item, ...prev];
//         return next.slice(0, 10);
//       });
//     } catch (e: any) {
//       showToast(e?.message || "Scan error");
//     } finally {
//       setIsScanning(false);
//     }
//   }

//   async function onRunNx(n: number) {
//     const p = prompt;
//     if (!p.trim()) {
//       showToast("Enter a prompt first");
//       return;
//     }

//     setIsScanning(true);
//     try {
//       for (let i = 0; i < n; i++) {
//         const data = await scanOnce(p);
//         setScanResult(data);

//         setHistory((prev) => {
//           const item: HistoryItem = {
//             id: uid(),
//             ts: nowLabel(),
//             prompt: p,
//             result: data,
//           };
//           const next = [item, ...prev];
//           return next.slice(0, 10);
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
//     if (!scanResult) {
//       showToast("No scan result to copy");
//       return;
//     }
//     await copyToClipboard(latestJson);
//     showToast("Copied JSON");
//   }

//   function onLoadFromHistory(item: HistoryItem) {
//     setPrompt(item.prompt);
//     setScanResult(item.result);
//     showToast("Loaded from history");
//   }

//   return (
//     <div style={{ maxWidth: 980, margin: "24px auto", padding: "0 16px", fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial" }}>
//       <h1 style={{ marginBottom: 6 }}>SentinelGate UI</h1>
//       <div style={{ color: "#555", marginBottom: 16 }}>
//         Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.
//       </div>

//       {toast && (
//         <div style={{ padding: "10px 12px", background: "#111", color: "white", borderRadius: 10, display: "inline-block", marginBottom: 12 }}>
//           {toast}
//         </div>
//       )}

//       <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 12 }}>
//         <input
//           value={prompt}
//           onChange={(e) => setPrompt(e.target.value)}
//           placeholder={`Try: "shipment tracking status for order 8842 from carrier"`}
//           style={{ flex: 1, padding: "12px 12px", borderRadius: 10, border: "1px solid #ddd" }}
//         />
//         <button
//           onClick={onScan}
//           disabled={isScanning}
//           style={{ padding: "12px 14px", borderRadius: 10, border: "1px solid #ddd", cursor: "pointer" }}
//         >
//           {isScanning ? "Scanning..." : "Scan"}
//         </button>
//         <button
//           onClick={() => onRunNx(10)}
//           disabled={isScanning}
//           style={{ padding: "12px 14px", borderRadius: 10, border: "1px solid #ddd", cursor: "pointer" }}
//         >
//           Run 10x
//         </button>
//       </div>

//       <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 18 }}>
//         <button
//           onClick={onCopyJson}
//           disabled={!scanResult}
//           style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid #ddd", cursor: scanResult ? "pointer" : "not-allowed" }}
//         >
//           Copy JSON
//         </button>

//         <button
//           onClick={() => setHistory([])}
//           disabled={history.length === 0}
//           style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid #ddd", cursor: history.length ? "pointer" : "not-allowed" }}
//         >
//           Clear History
//         </button>
//       </div>

//       <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 16 }}>
//         <div style={{ border: "1px solid #eee", borderRadius: 14, padding: 14 }}>
//           <h2 style={{ marginTop: 0 }}>Scan Result</h2>

//           {!scanResult ? (
//             <div style={{ color: "#666" }}>Run a scan to see output.</div>
//           ) : (
//             <>
//               <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 10 }}>
//                 <div style={{ fontWeight: 700 }}>
//                   {scanResult.decision} • {scanResult.layer_caught}
//                 </div>
//                 <div style={{ color: "#666" }}>{scanResult.reason}</div>
//               </div>

//               <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 10 }}>
//                 <div>
//                   <div style={{ fontSize: 12, color: "#777" }}>Action</div>
//                   <div style={{ fontWeight: 600 }}>{scanResult.action}</div>
//                 </div>
//                 <div>
//                   <div style={{ fontSize: 12, color: "#777" }}>Gate latency</div>
//                   <div style={{ fontWeight: 600 }}>{scanResult.gate_latency_ms} ms</div>
//                 </div>
//               </div>

//               <div style={{ marginBottom: 10 }}>
//                 <div style={{ fontSize: 12, color: "#777" }}>Original prompt</div>
//                 <div style={{ fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas", background: "#fafafa", padding: 10, borderRadius: 10, border: "1px solid #eee" }}>
//                   {scanResult.original_prompt ?? "(not returned)"}
//                 </div>
//               </div>

//               <div style={{ marginBottom: 10 }}>
//                 <div style={{ fontSize: 12, color: "#777" }}>Sanitized prompt</div>
//                 <div style={{ fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas", background: "#fafafa", padding: 10, borderRadius: 10, border: "1px solid #eee" }}>
//                   {scanResult.clean_prompt ?? "(not returned)"}
//                 </div>
//               </div>

//               <div>
//                 <div style={{ fontSize: 12, color: "#777" }}>Debug</div>
//                 <div style={{ fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas", background: "#fafafa", padding: 10, borderRadius: 10, border: "1px solid #eee", whiteSpace: "pre-wrap" }}>
//                   similarity: {scanResult.debug?.similarity ?? "n/a"} • margin: {scanResult.debug?.margin ?? "n/a"}
//                 </div>
//               </div>

//               <div style={{ marginTop: 12 }}>
//                 <div style={{ fontSize: 12, color: "#777" }}>Raw JSON</div>
//                 <pre style={{ background: "#0b1020", color: "#e8e8e8", padding: 12, borderRadius: 12, overflowX: "auto" }}>
//                   {latestJson}
//                 </pre>
//               </div>
//             </>
//           )}
//         </div>

//         <div style={{ border: "1px solid #eee", borderRadius: 14, padding: 14 }}>
//           <h2 style={{ marginTop: 0 }}>History (last 10)</h2>
//           {history.length === 0 ? (
//             <div style={{ color: "#666" }}>No scans yet.</div>
//           ) : (
//             <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
//               {history.map((h) => (
//                 <button
//                   key={h.id}
//                   onClick={() => onLoadFromHistory(h)}
//                   style={{
//                     textAlign: "left",
//                     padding: 10,
//                     borderRadius: 12,
//                     border: "1px solid #eee",
//                     background: "white",
//                     cursor: "pointer",
//                   }}
//                 >
//                   <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
//                     <div style={{ fontWeight: 700 }}>
//                       {h.result.decision} • {h.result.layer_caught}
//                     </div>
//                     <div style={{ color: "#777", fontSize: 12 }}>{h.ts}</div>
//                   </div>
//                   <div style={{ color: "#555", fontSize: 13, marginTop: 6, lineHeight: 1.25 }}>
//                     {h.prompt}
//                   </div>
//                   <div style={{ color: "#777", fontSize: 12, marginTop: 6 }}>
//                     reason: {h.result.reason} • latency: {h.result.gate_latency_ms} ms
//                   </div>
//                 </button>
//               ))}
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

import { useMemo, useState } from "react";
import "./App.css";

type ScanResponse = {
  decision: "PASSED" | "BLOCKED";
  layer_caught: "L0" | "L1" | "L2" | "UNKNOWN";
  reason: string;
  gate_latency_ms: number;
  action: "SEND_TO_LLM" | "REJECT_REQUEST";
  original_prompt?: string;
  clean_prompt?: string;
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

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const latestJson = useMemo(() => {
    return scanResult ? JSON.stringify(scanResult, null, 2) : "";
  }, [scanResult]);

  function showToast(msg: string) {
    setToast(msg);
    window.setTimeout(() => setToast(null), 1600);
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

  return (
    <div className="bg">
      <div className="shell">
        <header className="top">
          <div>
            <div className="brand">
              <div className="logo">SG</div>
              <div>
                <h1>SentinelGate</h1>
                <p>Enterprise “cheap-first” guardrail demo — scan prompts before sending to an expensive LLM.</p>
              </div>
            </div>
          </div>

          <div className="rightStats">
            <div className="kpi">
              <div className="kpiLabel">Status</div>
              <div className="kpiValue">{scanResult ? scanResult.decision : "—"}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Layer</div>
              <div className="kpiValue">{scanResult ? scanResult.layer_caught : "—"}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Latency</div>
              <div className="kpiValue">{scanResult ? `${scanResult.gate_latency_ms} ms` : "—"}</div>
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
                Tip: Try junk (“hi”), noise (“tell me a joke”), domain (“shipment delay status”), and off-domain (“reset my password”).
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
              <div className="empty">
                Run a scan to see the decision, reasoning, and debug metrics.
              </div>
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
                    <div className="metricValue">{scanResult.debug?.similarity ?? "n/a"}</div>
                  </div>
                  <div className="metric">
                    <div className="metricLabel">Margin</div>
                    <div className="metricValue">{scanResult.debug?.margin ?? "n/a"}</div>
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

        <footer className="foot">
          <span>SentinelGate • Supply Chain domain config • tau = 0.10</span>
        </footer>
      </div>
    </div>
  );
}
