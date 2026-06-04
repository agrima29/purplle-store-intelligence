import "./ZoneChart.css";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from "recharts";

export default function ZoneChart({ data = {} }) {

  const chartData = Object.entries(data).map(
    ([zone, revenue]) => ({
      zone,
      revenue
    })
  );

  const COLORS = [
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
    "#F59E0B",
    "#10B981",
    "#EF4444"
  ];

  return (
    <div className="zone-container">

      <div className="section-header">
        <h2>Revenue by Zone</h2>

        <p>
          Revenue contribution by store area
        </p>
      </div>

      <div className="zone-chart-card">

        <ResponsiveContainer
          width="100%"
          height={420}
        >
          <PieChart>

            <Pie
              data={chartData}
              dataKey="revenue"
              nameKey="zone"
              cx="50%"
              cy="50%"
              outerRadius={140}
              label
            >
              {chartData.map(
                (entry, index) => (
                  <Cell
                    key={index}
                    fill={
                      COLORS[
                        index % COLORS.length
                      ]
                    }
                  />
                )
              )}
            </Pie>

            <Tooltip />

            <Legend />

          </PieChart>
        </ResponsiveContainer>

      </div>

    </div>
  );
}