import "./Funnel.css";
import { FaStore, FaSearch, FaCashRegister, FaShoppingBag } from "react-icons/fa";

export default function Funnel({ funnel }) {

  if (!funnel || !funnel.stages) {
    return null;
  }

  const stages = funnel.stages;

  const icons = {
    entry: <FaStore />,
    browse: <FaSearch />,
    checkout: <FaCashRegister />,
    purchase: <FaShoppingBag />
  };

  return (
    <div className="funnel-container">

      <div className="section-header">
        <h2>Customer Conversion Funnel</h2>
        <p>
          Customer journey through the store
        </p>
      </div>

      <div className="funnel-grid">

        {stages.map((stage, index) => (
          <div key={index} className="funnel-card">

            <div className="funnel-icon">
              {icons[stage.stage]}
            </div>

            <h3>{stage.label}</h3>

            <div className="funnel-count">
              {stage.count}
            </div>

            {stage.pct_of_entry !== null && (
              <div className="funnel-percentage">
                {stage.pct_of_entry}%
              </div>
            )}

            {stage.dropoff !== undefined &&
              stage.dropoff !== null && (
              <div className="funnel-dropoff">
                Dropoff: {stage.dropoff}%
              </div>
            )}

            {index !== stages.length - 1 && (
              <div className="funnel-arrow">
                ↓
              </div>
            )}

          </div>
        ))}

      </div>

      {funnel.purchase_note && (
        <div className="funnel-note">
          {funnel.purchase_note}
        </div>
      )}

    </div>
  );
}