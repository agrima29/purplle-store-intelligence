import { useEffect, useState } from "react";
import API from "../../api/api";

import Navbar from "../../components/Navbar/Navbar";

export default function InsightsPage() {

  const [insights, setInsights] =
    useState(null);

  useEffect(() => {

    API.get("/insights")
      .then((res) =>
        setInsights(res.data)
      );

  }, []);

  return (

    <div className="dashboard">

      <Navbar />

      <div className="hero-section">

        <h1>
          Business Insights Center
        </h1>

        <p>
          Actionable store intelligence
          generated from customer and
          sales data.
        </p>

      </div>

      {insights &&
        insights.insights.map(
          (item, index) => (

            <div
              key={index}
              className="insight-card"
            >

              <h3>
                {item.title}
              </h3>

              <p>
                {item.insight}
              </p>

            </div>
          )
        )}

    </div>
  );
}