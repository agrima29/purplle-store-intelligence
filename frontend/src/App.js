import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home/Home";
import Dashboard from "./pages/Dashboard/Dashboard";
import Journey from "./pages/Journey/Journey";
import InsightsPage from "./pages/InsightsPage/InsightsPage";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/journey"
          element={<Journey />}
        />

        <Route
          path="/insights"
          element={<InsightsPage />}
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;