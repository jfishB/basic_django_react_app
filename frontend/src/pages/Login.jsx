import Form from "../components/Form"
import { useNavigate } from "react-router-dom"

function Login() {
    const navigate = useNavigate()

    return <Form route="/api/token/" method="login" onSuccess={() => navigate("/home")}/>
}

export default Login