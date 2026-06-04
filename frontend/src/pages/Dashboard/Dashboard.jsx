import { useEffect, useState } from "react";
import API from "../../api/api";

import KPICard from "../../components/KPICard/KPICard";
import RevenueChart from "../../components/RevenueChart/RevenueChart";
import Footfall from "../../components/Footfall/Footfall";
import Funnel from "../../components/Funnel/Funnel";
import JourneySearch from "../../components/JourneySearch/JourneySearch";
import Navbar from "../../components/Navbar/Navbar";
import ZoneChart from "../../components/ZoneChart/ZoneChart";
import Footer from "../../components/Footer/Footer";

import "./Dashboard.css";

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [funnel, setFunnel] = useState(null);

  useEffect(() => {
    loadData();
    
  }, []);

  const loadData = async () => {
    try {
      const metricsRes = await API.get("/metrics");
      const insightsRes = await API.get("/insights");
      const funnelRes = await API.get("/funnel");

    

      setMetrics(metricsRes.data);
      setFunnel(funnelRes.data);
    } catch (err) {
      console.log(err);
    }
  };

  if (!metrics) {
    return (
        <div className="loading-screen">
        <div className="loader"></div>
        <h2>Loading Store Intelligence...</h2>
        </div>
    );
 }

  return (
    <div className="dashboard">

        <Navbar />

        <div className="hero-section">

            <h1>
                Store Performance Dashboard
            </h1>

            <p>
                Transforming Store Activity into Actionable Business Insights
            </p>

        </div>

        <div className="store-summary">

          <div className="summary-box">
              <h4>Store</h4>
              <p>{metrics.store}</p>
          </div>

          <div className="summary-box">
              <h4>Date</h4>
              <p>10 Apr 2026</p>
          </div>

          <div className="summary-box">
              <h4>Top Zone</h4>
              <p>{metrics.intelligence.top_zone_by_revenue}</p>
          </div>

          <div className="summary-box">
              <h4>Top Salesperson</h4>
              <p>{metrics.intelligence.top_salesperson}</p>
          </div>

        </div>

      

      <div className="kpi-grid">

        <KPICard
          title="Total GMV"
          value={`₹${metrics.full_day.total_gmv_inr}`}
        />

        <KPICard
          title="Orders"
          value={metrics.full_day.total_transactions}
        />

        <KPICard
          title="Customers"
          value={metrics.full_day.unique_customers}
        />

        <KPICard
          title="Occupancy"
          value={metrics.video_clip.in_store}
        />

        <KPICard
          title="Peak Hour"
          value={metrics.full_day.peak_sales_hour}
        />

        <KPICard
          title="Conversion %"
          value={metrics.video_clip.conversion_pct + "%"}
        />

        
      </div>

      <div id="analytics">
        <RevenueChart
            data={metrics.full_day.department_revenue}
        />
    </div>

    

    <ZoneChart
        data={metrics.full_day.revenue_by_zone}
    />

    <Footfall
        entries={metrics.video_clip.entries}
        exits={metrics.video_clip.exits}
        occupancy={metrics.video_clip.in_store}
    />

    {funnel && (
        <Funnel funnel={funnel} />
    )}
      

      

     

    
        <div id="journey">
            <JourneySearch />
        </div>

        <Footer />

    </div>
  );
}