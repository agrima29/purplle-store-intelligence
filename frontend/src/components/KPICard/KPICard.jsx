import "./KPICard.css";
import { motion } from "framer-motion";

export default function KPICard({
  title,
  value
}) {

  return (

    <motion.div
      className="kpi-card"
      whileHover={{
        y: -8,
        scale: 1.03
      }}
    >

      <h3>{title}</h3>

      <p>{value}</p>

    </motion.div>
  );
}