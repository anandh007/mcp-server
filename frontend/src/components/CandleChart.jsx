import {
  ResponsiveContainer,
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  CandlestickSeries,
} from "recharts";

export default function CandleChart({ data }) {
  // Format data for recharts
  const formatted = data.map((c) => ({
    datetime: c.datetime,
    open: c.open,
    high: c.high,
    low: c.low,
    close: c.close,
  }));

  return (
    <div className="w-full h-96 bg-white/20 dark:bg-white/5 backdrop-blur-xl p-4 rounded-2xl">
      <h2 className="text-xl font-semibold mb-4">BTC/USDT Candlestick Chart</h2>

      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
          <XAxis dataKey="datetime" hide />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <CandlestickSeries
            dataKey="close"
            openKey="open"
            closeKey="close"
            highKey="high"
            lowKey="low"
            fill="#22c55e"
            stroke="#16a34a"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
