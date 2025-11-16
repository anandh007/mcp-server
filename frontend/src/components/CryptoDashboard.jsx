import React, { useEffect, useState } from "react";

// Base64 logo
const logo =
  "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzYiIGhlaWdodD0iNzYiIHZpZXdCb3g9IjAgMCA3NiA3NiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTM4IDc2QzU4LjE0MjEgNzYgNzYgNTguMTQyMSA3NiAzOEM3NiAxNy44NTc5IDU4LjE0MjEgMCAzOCAwQzE3Ljg1NzkgMCAwIDE3Ljg1NzkgMCAzOEMwIDU4LjE0MjEgMTcuODU3OSA3NiAzOCA3NloiIGZpbGw9IiM0MjQyRDgiLz4KPHBhdGggZD0iTTM4IDE5QzI3LjUwMzIgMTkgMTkgMjcuNTAzMiAxOSA0OEMxOSA2OC40OTY4IDI3LjUwMzIgNzggMzggNzhDMzUuMjA5MyA3OCAzMi45MjA2IDc3LjE0NyAzMS4wMDAzIDc1LjU5MjJDMjkuMDgwMSA3My45NjY4IDI3LjUgNzEuMTY1NCAyNy41IDY4QzI3LjUgNTcuNDAyOCAzNS43MzM5IDQ5LjE2NjEgNDYgNDlWNDNIMzAuNVYzNEg0NlYyOEgzMFYxOUg0Nkw0NiAxOUMzNi45NTI4IDE5IDM4IDE5IDM4IDE5WiIgZmlsbD0iI2ZmZiIvPgo8L3N2Zz4=";

export default function CryptoDashboard() {
  const [btc, setBtc] = useState(null);
  const [eth, setEth] = useState(null);
  const [priceHistory, setPriceHistory] = useState([]);
  const [wsStatus, setWsStatus] = useState("Connecting...");
  const [ws, setWs] = useState(null);
  const [darkMode, setDarkMode] = useState(true);

  /* DARK MODE */
  const toggleDark = () => {
    const newState = !darkMode;
    setDarkMode(newState);

    if (newState) document.documentElement.classList.add("dark");
    else document.documentElement.classList.remove("dark");
  };

  /* WEBSOCKET */
  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/api/ws");

    socket.onopen = () => {
      setWsStatus("Connected");
      setWs(socket);
    };
    socket.onerror = () => setWsStatus("Error");
    socket.onclose = () => setWsStatus("Closed");

    return () => socket.close();
  }, []);

  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data);

      if (data.pair === "BTC/USDT") {
        setBtc(data.ticker);

        setPriceHistory((prev) => [
          ...prev.slice(-60),
          {
            time: new Date().toLocaleTimeString(),
            price: data.ticker.last,
          },
        ]);
      }

      if (data.pair === "ETH/USDT") {
        setEth(data.ticker);
      }
    };
  }, [ws]);

  /* SVG LINE CHART */
  const renderChart = () => {
    if (priceHistory.length < 2) return null;

    const prices = priceHistory.map((p) => p.price);
    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const height = 240;
    const step = 12;

    const scaleY = (value) =>
      height - ((value - min) / (max - min)) * height;

    return priceHistory.map((p, i) => {
      if (i === 0) return null;
      const prev = priceHistory[i - 1];

      return (
        <line
          key={i}
          x1={(i - 1) * step}
          y1={scaleY(prev.price)}
          x2={i * step}
          y2={scaleY(p.price)}
          stroke="#4ade80"
          strokeWidth="3"
          strokeLinecap="round"
        />
      );
    });
  };

  return (
    <div
      className="min-h-screen w-full p-6 
      bg-gradient-to-br from-blue-50 to-purple-100
      dark:from-gray-900 dark:to-black
      text-gray-900 dark:text-white transition-all"
    >
      {/* NAVBAR */}
      <div className="flex justify-between items-center mb-10">
        <div className="flex items-center gap-3">
          <img src={logo} className="h-12 w-12" />
          <h1 className="text-3xl font-extrabold">Crypto Dashboard</h1>
        </div>

        <button
          onClick={toggleDark}
          className="px-4 py-2 rounded-xl bg-black/10 dark:bg-white/10 
          border border-white/20 backdrop-blur-xl shadow-lg hover:scale-105 
          transition text-black dark:text-white"
        >
          {darkMode ? "🌞 Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      {/* GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* BTC CARD */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-2">BTC/USDT</h2>
          <p className="text-sm opacity-70 mb-4">{wsStatus}</p>
          {btc ? (
            <div className="space-y-1 text-lg">
              <p>
                💰 <b>${btc.last.toLocaleString()}</b>
              </p>
              <p>📈 High: {btc.high}</p>
              <p>📉 Low: {btc.low}</p>
              <p>🔄 Change: {btc.percentage}%</p>
            </div>
          ) : (
            <p>Loading BTC...</p>
          )}
        </div>

        {/* BTC LINE CHART */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-4">BTC Live Chart</h2>
          <div className="h-72 rounded-xl p-3 bg-white/10 dark:bg-white/5 backdrop-blur-xl">
            <svg width="100%" height="100%">{renderChart()}</svg>
          </div>
        </div>

        {/* ETH */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-semibold mb-3">ETH/USDT</h2>
          {eth ? (
            <div className="space-y-1 text-lg">
              <p>
                💰 <b>${eth.last.toLocaleString()}</b>
              </p>
              <p>📈 High: {eth.high}</p>
              <p>📉 Low: {eth.low}</p>
              <p>🔄 Change: {eth.percentage}%</p>
            </div>
          ) : (
            <p>Loading ETH...</p>
          )}
        </div>
      </div>
    </div>
  );
}
