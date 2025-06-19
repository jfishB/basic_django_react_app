import { Navigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem(ACCESS_TOKEN);
  
  if (!token) {
    return <Navigate to="/welcome" />;
  }
  
  return children;
}

export default ProtectedRoute;