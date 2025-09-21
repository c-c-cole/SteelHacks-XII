import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import App from "./App";
import Profile from "./Profile";
import About from "./About";  

function MainRouter() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/about">About</Link> 
      </nav>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}

export default MainRouter;
