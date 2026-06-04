import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import "./Home.css";

export default function Home() {

  const navigate = useNavigate();

  return (

    <div className="home">

      <motion.div
        className="overlay"
        initial={{
          opacity: 0,
          y: 50
        }}
        animate={{
          opacity: 1,
          y: 0
        }}
        transition={{
          duration: 0.8
        }}
      >

        <h1>
          Purplle Store Intelligence
        </h1>

        <p>
          Customer Movement Analytics •
          Conversion Tracking •
          Sales Intelligence
        </p>

        

        <div className="home-buttons">

          <button
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Explore Analytics
          </button>

          <button
            className="secondary-btn"
            onClick={() =>
              navigate("/insights")
            }
          >
            View Insights
          </button>

        </div>

      </motion.div>

    </div>
  );
}