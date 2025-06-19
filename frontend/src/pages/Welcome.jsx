import { Link } from "react-router-dom";
import "../styles/Welcome.css";

function Welcome() {
  return (
    <div className="welcome">
      <h1>Welcome to Jump Analyzer</h1>
      <div className="auth-buttons">
        <Link to="/login" className="auth-button">Login</Link>
        <Link to="/register" className="auth-button">Register</Link>
      </div>
    </div>
  );
}

export default Welcome;