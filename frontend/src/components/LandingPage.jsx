import React, { useState } from "react";

export default function BargainHunterApp() {
  // State untuk mengontrol Tour Blueprint
  const [activeStep, setActiveStep] = useState(0);

  const tourSteps = [
    { step: "Step 1", title: "Set Target Parameters", desc: "Paste the direct marketplace query or SKU category URL into the workflow system.", icon: "fa-crosshairs" },
    { step: "Step 2", title: "Secure Data Extraction", desc: "Automated cloud infrastructure pulls text-based price listings safely and reliably.", icon: "fa-spider" },
    { step: "Step 3", title: "Compliance Audit", desc: "The processing module benchmarks data fields against historical records and margins.", icon: "fa-scale-balanced" },
    { step: "Step 4", title: "Executive Report", desc: "Get clean, high-level structural advice (MAINTAIN / ADJUST / ACTION) ready for decision makers.", icon: "fa-file-contract" },
  ];

  const handleNextTour = () => {
    if (activeStep < tourSteps.length - 1) setActiveStep(activeStep + 1);
  };

  const handlePrevTour = () => {
    if (activeStep > 0) setActiveStep(activeStep - 1);
  };

  return (
    <div className="font-sans text-slate-800 bg-white min-h-screen selection:bg-blue-100">
        <div className="animate-fade-in">
          {/* ── NAVBAR ── */}
          <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between w-full px-6 md:px-12 py-4 bg-white/90 backdrop-blur-md border-b border-slate-200">
            <div className="flex items-center gap-2 text-xl font-black text-slate-900 tracking-tight">
              <i className="fa-solid fa-bullseye text-blue-600"></i> BargainHunter
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors">Capabilities</a>
              <a href="#how-it-works" className="text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors">No-Code Workflow</a>
              <a href="#metrics" className="text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors">Compliance Results</a>
              <a href="#faq" className="text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors">FAQ</a>
            </div>
            <div className="flex items-center gap-5">
              <a
                href="/dashboard"
                className="px-5 py-2.5 text-sm font-bold text-white bg-blue-600 border border-blue-700 rounded-lg transition-all hover:bg-blue-700 shadow-sm"
              >
                Get started
              </a>
            </div>
          </nav>

          {/* ── HERO SECTION ── */}
          <section className="text-center pt-40 pb-24 px-6 bg-white border-b border-slate-100">
            <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-100 px-4 py-1.5 rounded-full text-xs text-blue-600 font-bold uppercase tracking-wider mb-6">
              <i className="fa-solid fa-lock"></i> Automated B2B Price Compliance
            </div>
            <h1 className="text-4xl md:text-6xl font-black leading-[1.1] max-w-4xl mx-auto mb-6 text-slate-900 tracking-tight">
              Deploy Price Surveillance Flows Without Code
            </h1>
            <p className="text-lg text-slate-500 max-w-2xl mx-auto mb-10 leading-relaxed">
              Set up autonomous monitoring pipelines, detect market positioning anomalies, and secure margins using an intuitive, developer-free infrastructure.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <a
                href="/dashboard"
                className="bg-blue-600 text-white px-8 py-3.5 rounded-lg font-bold text-[15px] inline-flex items-center gap-2 border border-blue-700 transition hover:bg-blue-700 shadow-md shadow-blue-500/20"
              >
                Launch Automation Flow <i className="fa-solid fa-arrow-right"></i>
              </a>
              <a href="#how-it-works" className="bg-white border border-slate-300 text-slate-700 px-8 py-3.5 rounded-lg font-bold text-[15px] inline-flex items-center gap-2 transition hover:bg-slate-50">
                See Blueprint
              </a>
            </div>
          </section>

          {/* ── STATS ROW ── */}
          <section className="grid grid-cols-2 md:grid-cols-4 bg-slate-50 border-b border-slate-200">
            {[
              { val: "99.9%", label: "Guaranteed Uptime" },
              { val: "<30s", label: "Verification Speed" },
              { val: "100%", label: "No-Code System" },
              { val: "24/7", label: "Continuous Audit" }
            ].map((stat, idx) => (
              <div key={idx} className="text-center py-12 px-6 border-r border-slate-200 last:border-r-0">
                <div className="text-4xl md:text-5xl font-black text-slate-900 mb-2 tracking-tight">{stat.val}</div>
                <div className="text-xs text-slate-500 font-bold uppercase tracking-widest">{stat.label}</div>
              </div>
            ))}
          </section>

          {/* ── FEATURES GRID ── */}
          <section id="features" className="pt-24 pb-12 px-6 max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <span className="inline-block text-blue-600 text-sm font-bold uppercase tracking-widest mb-3">Platform Features</span>
              <h2 className="text-3xl md:text-4xl font-black mb-4 text-slate-900 tracking-tight">Enterprise Price Guardrails</h2>
              <p className="text-base text-slate-500 max-w-2xl mx-auto leading-relaxed">Complete toolkit designed for business operations, legal officers, and commerce executives to track pricing compliance.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 border-t border-l border-slate-200">
              {[
                { icon: "fa-shield-halved", title: "Intelligent Tracking", desc: "Extract precise product data, SKU structures, and current stock status across multi-channel environments instantly." },
                { icon: "fa-chart-pie", title: "Anomaly Auditing", desc: "Instantly flag violations of minimum advertised pricing (MAP) or deep competitive drops with high precision." },
                { icon: "fa-gavel", title: "Rule Validation", desc: "Run pricing intelligence past built-in business governance guardrails to secure margin safety and legal compliance." },
                { icon: "fa-sliders", title: "Visual Flow Builder", desc: "Orchestrate complex target verification structures completely code-free via a drag-and-drop dashboard." }
              ].map((feature, idx) => (
                <div key={idx} className="bg-white border-r border-b border-slate-200 p-10 transition hover:bg-slate-50">
                  <div className="w-14 h-14 bg-slate-100 border border-slate-200 rounded-xl flex items-center justify-center text-2xl text-blue-600 mb-6">
                    <i className={`fa-solid ${feature.icon}`}></i>
                  </div>
                  <h3 className="text-xl font-bold mb-3 text-slate-900">{feature.title}</h3>
                  <p className="text-sm text-slate-500 leading-relaxed">{feature.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* ── HOW IT WORKS (ERGONOMIC & COMPACT VERSION) ── */}
          <section id="how-it-works" className="py-16 md:py-20 px-4 md:px-6">
            {/* Kunci Jangkauan Desktop: membatasi max-w-2xl untuk navigasi & card */}
            <div className="max-w-2xl mx-auto">

              {/* Top Controls - Sekarang rata kiri-kanan sejajar dengan lebar Card! */}
              <div className="flex items-center justify-between mb-5">
                <button className="flex items-center gap-2 text-blue-600 font-bold text-sm bg-blue-50 px-4 py-2 rounded-xl transition hover:bg-blue-100">
                  <i className="fa-solid fa-border-all"></i> All tours
                </button>

                <div className="hidden md:block flex-1 mx-6 bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-blue-600 h-full rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${((activeStep + 1) / tourSteps.length) * 100}%` }}
                  ></div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={handlePrevTour}
                    disabled={activeStep === 0}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-slate-50 text-slate-400 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm"
                  >
                    <i className="fa-solid fa-chevron-left"></i>
                  </button>
                  <button
                    onClick={handleNextTour}
                    disabled={activeStep === tourSteps.length - 1}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-blue-50 text-blue-600 hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm"
                  >
                    <i className="fa-solid fa-chevron-right"></i>
                  </button>
                </div>
              </div>

              {/* Container Luar */}
              <div className="bg-[#8b95a6] rounded-[24px] md:rounded-[32px] p-4 md:p-8 w-full shadow-lg">

                {/* Container Dalam (w-full agar mengisi lebar max-w-2xl di atas) */}
                <div className="w-full bg-white/10 backdrop-blur-sm border border-white/20 rounded-[20px] md:rounded-[24px] p-6 md:p-8 text-center shadow-xl">
                  <h3 className="text-xl md:text-2xl font-black text-slate-900 mb-1 tracking-tight">The 4-Step Automation Flow</h3>
                  <p className="text-slate-700 text-sm font-medium mb-6">How our secure system processes competitive pricing data.</p>

                  <div className="space-y-3 md:space-y-4 text-left relative min-h-[260px] md:min-h-[270px]">
                    {tourSteps.map((item, idx) => {
                      const isActive = idx === activeStep;

                      return (
                        <div
                          key={idx}
                          onClick={() => setActiveStep(idx)}
                          className={`flex items-start gap-4 transition-all duration-500 cursor-pointer ${isActive ? 'opacity-100 scale-100' : 'opacity-40 hover:opacity-70 scale-95'}`}
                        >
                          {/* ── ICON ── */}
                          <div className={`w-10 h-10 md:w-12 md:h-12 shrink-0 rounded-xl flex items-center justify-center text-lg md:text-xl mt-0.5 transition-colors duration-500 overflow-hidden relative ${isActive ? 'bg-slate-900 text-white shadow-md' : 'border-2 border-slate-700 text-slate-800'}`}>

                            {/* 1. Target */}
                            {idx === 0 && (
                              <i className={`fa-solid ${item.icon} transition-all duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)] ${isActive ? 'rotate-0 scale-125' : '-rotate-45 scale-75 opacity-80'}`}></i>
                            )}

                            {/* 2. Laba-laba */}
                            {idx === 1 && (
                              <i className={`fa-solid ${item.icon} transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] ${isActive ? 'translate-y-0 opacity-100 scale-110' : '-translate-y-6 opacity-0 scale-90'}`}></i>
                            )}

                            {/* 3. Neraca */}
                            {idx === 2 && (
                              <i className={`fa-solid ${item.icon} transition-all duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)] origin-bottom ${isActive ? 'rotate-0 scale-110' : '-rotate-[25deg] scale-90 opacity-80'}`}></i>
                            )}

                            {/* 4. Kertas Grafik */}
                            {idx === 3 && (
                              <div className="relative w-full h-full flex items-center justify-center">
                                <i className={`fa-regular fa-file absolute transition-all duration-500 ease-in-out ${isActive ? 'opacity-0 scale-50 rotate-12' : 'opacity-100 scale-100 rotate-0'}`}></i>
                                <i className={`fa-solid ${item.icon} absolute transition-all duration-500 delay-100 ease-[cubic-bezier(0.34,1.56,0.64,1)] ${isActive ? 'opacity-100 scale-110 rotate-0' : 'opacity-0 scale-50 -rotate-12'}`}></i>
                              </div>
                            )}

                          </div>

                          {/* Text Content */}
                          <div className="flex-1">
                            <div className="text-[11px] md:text-xs font-bold text-slate-700 mb-0.5 uppercase tracking-wide">{item.step}</div>
                            <div className={`font-bold text-slate-900 leading-tight transition-all duration-300 ${isActive ? 'text-lg mb-1' : 'text-base mb-0'}`}>{item.title}</div>

                            {/* Description */}
                            <div className={`overflow-hidden transition-all duration-500 ease-in-out ${isActive ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'}`}>
                              <p className="text-[13px] md:text-sm text-slate-800 font-medium leading-relaxed pb-1">{item.desc}</p>
                            </div>
                          </div>
                        </div>
                      )
                    })}
                  </div>

                  {/* ── TOMBOL START DEMO ── */}
                  <div className={`transition-all duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)] overflow-hidden ${activeStep === 3 ? 'max-h-24 opacity-100 mt-5 scale-100' : 'max-h-0 opacity-0 mt-0 scale-95'}`}>
                    <a
                      href="/dashboard"
                      className="bg-[#0f172a] text-white w-full py-3 md:py-3.5 rounded-xl font-bold text-base hover:bg-black transition-colors flex items-center justify-center gap-2 shadow-lg shadow-black/20"
                    >
                      Start Demo Flow <i className="fa-solid fa-arrow-right text-xs"></i>
                    </a>
                  </div>

                </div>
              </div>
            </div>
          </section>

          {/* ── METRICS BANNER ── */}
          <section id="metrics" className="py-24 px-6 bg-slate-900 text-center">
            <div className="max-w-5xl mx-auto">
              <span className="inline-block text-blue-400 text-sm font-bold uppercase tracking-widest mb-3">Audit Impact</span>
              <h2 className="text-3xl md:text-4xl font-black mb-12 text-white tracking-tight">Engineered for High Trust Operations</h2>

              <div className="grid grid-cols-1 md:grid-cols-3 border border-slate-700 rounded-2xl overflow-hidden bg-slate-800/50 backdrop-blur-sm">
                <div className="p-10 border-b md:border-b-0 md:border-r border-slate-700">
                  <div className="text-5xl font-black text-emerald-400 mb-2">94%</div>
                  <div className="text-xs text-slate-400 font-bold uppercase tracking-widest">Manual Labor Reduction</div>
                </div>
                <div className="p-10 border-b md:border-b-0 md:border-r border-slate-700">
                  <div className="text-5xl font-black text-emerald-400 mb-2">30s</div>
                  <div className="text-xs text-slate-400 font-bold uppercase tracking-widest">Audit Turnaround Time</div>
                </div>
                <div className="p-10">
                  <div className="text-5xl font-black text-emerald-400 mb-2">99.2%</div>
                  <div className="text-xs text-slate-400 font-bold uppercase tracking-widest">Data Accuracy Rating</div>
                </div>
              </div>
            </div>
          </section>

          {/* ── FAQ ── */}
          <section id="faq" className="py-24 px-6 max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <span className="inline-block text-blue-600 text-sm font-bold uppercase tracking-widest mb-3">FAQ</span>
              <h2 className="text-3xl md:text-4xl font-black mb-4 text-slate-900 tracking-tight">Frequently Asked Questions</h2>
            </div>
            <div className="space-y-4">
              <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
                <h4 className="text-lg font-bold text-slate-900 mb-2">Do I need engineering experience to use this?</h4>
                <p className="text-slate-500 text-sm leading-relaxed">No. The entire system is built with a strictly code-free interface allowing product and operational leads to schedule or run audit tracking independently.</p>
              </div>
              <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
                <h4 className="text-lg font-bold text-slate-900 mb-2">How safe is our internal pricing rulebook?</h4>
                <p className="text-slate-500 text-sm leading-relaxed">Extremely safe. Every rule checking engine operates strictly within secure database boundaries and does not expose corporate goals externally.</p>
              </div>
            </div>
          </section>

          {/* ── CTA BANNER ── */}
          <section id="launch" className="text-center py-24 px-6 bg-slate-50 border-t border-slate-200">
            <h2 className="text-3xl md:text-4xl font-black mb-4 text-slate-900 tracking-tight">Secure Your Pricing Infrastructure Today</h2>
            <p className="text-lg text-slate-500 mb-8">No deployment pipeline setup required. Immediate access.</p>
            <a
              href="/dashboard"
              className="bg-blue-600 text-white px-8 py-3.5 rounded-lg font-bold border border-blue-700 transition hover:bg-blue-700 shadow-md"
            >
              Open No-Code Dashboard System
            </a>
          </section>

          {/* ── FOOTER ── */}
          <footer className="bg-white py-12 px-6 text-center border-t border-slate-200">
            <div className="text-xl font-black text-slate-900 mb-4 tracking-tight">
              <i className="fa-solid fa-bullseye text-blue-600 mr-2"></i>BargainHunter
            </div>
            <p className="text-sm text-slate-500">&copy; 2026 BargainHunter Operations. Standardized B2B Intelligence Infrastructure.</p>
          </footer>
        </div>
    </div>
  );
}