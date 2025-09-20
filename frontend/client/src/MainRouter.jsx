import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import App from "./App";
import Profile from "./Profile";

function MainRouter() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  );
}

export default MainRouter;
