import {React, setState, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    const data = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password
    };

    console.log(data)

    await axios.post("http://localhost:5000/register", data)
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

        <label>First name</label>
        <input type="text" value={firstName} onChange={(e)=>setFirstName(e.target.value)}/>
        
        <label>Last name</label>
        <input type="text" value={lastName} onChange={(e)=>setLastName(e.target.value)}/>

        <label>Password</label>
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}/>

        <button type="button" onClick={() => handleSubmit()}>Register</button>
      </form>
    </div>
  );
};

export default Register;
