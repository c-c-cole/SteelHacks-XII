import { Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "./loginButton";
import LogoutButton from "./LogoutButton";

function NavBar() {
  const { isAuthenticated } = useAuth0();

  return (
    <div className="nav-bar">
      <Link to="/">Home</Link>
      <Link to="/about">About</Link> {/* Added About link */}
      {isAuthenticated && <Link to="/profile">Profile</Link>}

      <div className="auth-buttons">
        {isAuthenticated ? <LogoutButton /> : <LoginButton />}
      </div>
    </div>
  );
}

export default NavBar;
