import "./Navbar.css";
import {
  
} from "react-icons/fa";

export default function Navbar() {
  return (
    <nav className="navbar">

      <div className="navbar-left">
{/* 
        <div className="logo-container">
          <img
            src="/Purplle-logo.png"
            alt="Purplle Logo"
            className="purplle-logo"
          />
        </div> */}

        <div>
          <h1 className="navbar-title">
            Purplle Store Intelligence
          </h1>

          <p className="navbar-subtitle">
            Customer Movement Analytics • Conversion Tracking • Sales Intelligence
          </p>
        </div>

      </div>

      

      

    </nav>
  );
}