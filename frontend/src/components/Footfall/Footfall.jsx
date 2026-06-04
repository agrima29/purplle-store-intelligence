import "./Footfall.css";
import { FaSignInAlt, FaSignOutAlt, FaUsers } from "react-icons/fa";

export default function Footfall({
  entries = 0,
  exits = 0,
  occupancy = 0
}) {
  return (
    <div className="footfall-container">

      <div className="section-header">
        <h2>Store Footfall Analytics</h2>
        <p>Real-time customer movement inside the store</p>
      </div>

      <div className="footfall-grid">

        <div className="footfall-card">
          <div className="footfall-icon">
            <FaSignInAlt />
          </div>

          <h3>Entries</h3>

          <div className="footfall-value">
            {entries}
          </div>

          <p className="footfall-desc">
            Customers entered the store
          </p>
        </div>

        <div className="footfall-card">
          <div className="footfall-icon">
            <FaSignOutAlt />
          </div>

          <h3>Exits</h3>

          <div className="footfall-value">
            {exits}
          </div>

          <p className="footfall-desc">
            Customers exited the store
          </p>
        </div>

        <div className="footfall-card">
          <div className="footfall-icon">
            <FaUsers />
          </div>

          <h3>Current Occupancy</h3>

          <div className="footfall-value">
            {occupancy}
          </div>

          <p className="footfall-desc">
            Customers currently inside
          </p>
        </div>

      </div>

    </div>
  );
}