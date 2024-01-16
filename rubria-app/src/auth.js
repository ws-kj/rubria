import axios from "axios";
import { React, useState, useEffect } from "react";
import { Navigate, useLocation } from "react-router-dom";
const getUser = async () => {

  try {
    const response = await axios.get("http://localhost:5000/check_auth", {withCredentials: true});
    console.log(response.data);
    if(!response.data.logged_in || response.data.user === null) {
      return null;
    }
    return response.data.user;  
  } catch (error) {
      console.log(error);
      return null;
  };
};

function RequireAuth({children}) {
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    const verify = async () => {
      try {
        const res = await getUser();
        if(res) {
          setUser(res);
        } else {
          setError(true);
        }
      } catch (error) {
        console.error(error);
        setError(true);
      }
    }

    verify();
  }, []);


  if(!user) {
    if(!error) {
      return <div><h1>Loading...</h1></div>;
    } else {
      return <Navigate to="/login" state={{ from: location }} />;
    }
  }

  return children;
}

export {RequireAuth, getUser};
