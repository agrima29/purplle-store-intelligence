import "./RevenueChart.css";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from "recharts";

export default function RevenueChart({ data = {} }) {

  const chartData = Object.entries(data).map(
    ([department, revenue]) => ({
      department,
      revenue
    })
  );

  const colors = [
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
    "#F59E0B",
    "#10B981",
    "#EF4444"
  ];

  return (
    <div className="revenue-container">

      <div className="section-header">
        <h2>Revenue by Department</h2>
        <p>
          Department-wise revenue contribution
        </p>
      </div>

      <div className="chart-card">

        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <BarChart data={chartData}>

            <CartesianGrid
              strokeDasharray="3 3"
              opacity={0.15}
            />

            <XAxis
              dataKey="department"
              tick={{ fill: "#ffffff" }}
            />

            <YAxis
              tick={{ fill: "#ffffff" }}
            />

            <Tooltip
              contentStyle={{
                background: "#1f1f3a",
                border: "none",
                borderRadius: "12px",
                color: "white"
              }}
            />

            <Bar
              dataKey="revenue"
              radius={[8, 8, 0, 0]}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={index}
                  fill={
                    colors[index % colors.length]
                  }
                />
              ))}
            </Bar>

          </BarChart>
        </ResponsiveContainer>

      </div>

    </div>
  );
}