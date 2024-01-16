import { React, useState, useEffect } from "react";
import { RequireAuth } from "./auth.js"
import { BrowserRouter, Routes, Route, useNavigate, Navigate } from "react-router-dom";

import Home from "./Home";
import Register from "./Register";
import Login from "./Login";
import Dashboard from "./Dashboard";
import NotFound from "./NotFound";
/*
const ProtectedRoute = ({component: Component, ...rest}) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const verify = async () => {
      try {
        const user = await checkAuth();
        
        if(user === null || user === undefined || user.logged_in === false || user.user === null) {
          navigate("/login");
        }
        setUser(user); 
      } catch (error) {
        console.error(error);
        navigate("/login");
      }
    }

    verify();
  }, []);

  return (
    <Route {...rest}>
      {user != null ? <Component {...rest} user={user}/> : <Navigate to="/login" />}
    </Route>
  );
};*/

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/dashboard" element={<RequireAuth><Dashboard/></RequireAuth>}/>
        <Route path="*" element={<NotFound/>}/>
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
