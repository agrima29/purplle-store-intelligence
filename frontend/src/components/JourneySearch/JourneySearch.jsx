import { useState } from "react";
import API from "../../api/api";
import "./JourneySearch.css";

export default function JourneySearch() {

  const [trackId, setTrackId] = useState("");
  const [journey, setJourney] = useState(null);
  const [loading, setLoading] = useState(false);

  const searchJourney = async () => {

    if (!trackId) return;

    try {
      setLoading(true);

      const response = await API.get(
        `/journey/${trackId}`
      );

      setJourney(response.data);

    } catch (error) {
      console.error(error);
      alert("Journey not found");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="journey-container">

      <div className="section-header">
        <h2>Customer Journey Explorer</h2>

        <p>
          Search a customer track ID and
          visualize their movement through
          the store.
        </p>
      </div>

      <div className="journey-search-box">

        <input
          type="number"
          placeholder="Enter Track ID (e.g. 22)"
          value={trackId}
          onChange={(e) =>
            setTrackId(e.target.value)
          }
        />

        <button onClick={searchJourney}>
          Search Journey
        </button>

      </div>

      {loading && (
        <div className="journey-loading">
          Loading...
        </div>
      )}

      {journey && (

        <div className="journey-result">

          <h3>
            Customer #{journey.track_id}
          </h3>

          <div className="journey-path">

            {journey.journey?.map(
              (zone, index) => (
                <div
                  key={index}
                  className="journey-step"
                >
                  <div className="zone-card">
                    {zone}
                  </div>

                  {index !==
                    journey.journey.length - 1 && (
                    <div className="journey-arrow">
                      →
                    </div>
                  )}
                </div>
              )
            )}

          </div>

          <div className="journey-summary">

            <div className="summary-card">
              <h4>Total Events</h4>
              <p>
                {journey.total_events}
              </p>
            </div>

            <div className="summary-card">
              <h4>Track ID</h4>
              <p>
                {journey.track_id}
              </p>
            </div>

          </div>

        </div>

      )}

    </div>
  );
}