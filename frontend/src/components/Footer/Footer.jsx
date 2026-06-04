import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">

      <h3>Purplle Store Intelligence</h3>

      <p>
        AI-Powered Retail Analytics Platform
      </p>

      <div className="tech-stack">
        <span>YOLOv8</span>
        <span>ByteTrack</span>
        <span>FastAPI</span>
        <span>React</span>
        <span>SQLite</span>
      </div>

      <p className="footer-copy">
        Designed for Purplle's Next-Generation Store Analytics
      </p>

    </footer>
  );
}