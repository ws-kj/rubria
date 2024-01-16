import {React, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    const data = {
      email: email,
      password: password
    };

    console.log(data)

    await axios.post("http://localhost:5000/login", data, {withCredentials: true})
      .then(response => {
        console.log(response);

        navigate("/");
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div>
      <form>
        <label>Email</label>
        <input type="text" value={email} onChange={(e)=>setEmail(e.target.value)}/>

        <label>Password</label>
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}/>

        <button type="button" onClick={() => handleSubmit()}>Login</button>
      </form>
    </div>
  );
};

export default Login;
