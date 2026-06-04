import Navbar from "../../components/Navbar/Navbar";
import JourneySearch from "../../components/JourneySearch/JourneySearch";

export default function Journey() {

  return (

    <div className="dashboard">

      <Navbar />

      <div className="hero-section">

        <h1>
          Customer Journey Explorer
        </h1>

        <p>
          Track customer movement across
          the Purplle store.
        </p>

      </div>

      <JourneySearch />

    </div>
  );
}