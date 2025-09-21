import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Auth0Provider } from "@auth0/auth0-react";
import "./index.css";

import App from "./App.jsx";
import Profile from "./Profile.jsx";
import ProtectedRoute from "./ProtectedRoute.jsx";
import NavBar from "./NavBar.jsx";
import About from "./About.jsx";  // ✅ import About

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Auth0Provider
      domain={import.meta.env.VITE_AUTH0_DOMAIN}
      clientId={import.meta.env.VITE_AUTH0_CLIENT_ID}
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
    >
      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<App />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route path="/about" element={<About />} /> {/* ✅ Add this */}
        </Routes>
      </Router>
    </Auth0Provider>
  </StrictMode>
);
