import React, { useEffect } from "react";
import ls from "local-storage";
import { useDispatch } from "react-redux";
import { LOGIN_USER, LOGOUT_USER } from "../actions/types";
import Navbar from "./Navbar";

export default props => {
  const dispatch = useDispatch();

  useEffect(() => {
    // check localstorage to see if user is saved
    const userFromLocalStorage = ls.get("user");
    if (userFromLocalStorage) {
      dispatch({ type: LOGIN_USER, user: userFromLocalStorage });
    } else {
      // here to dispatch to loaded reducer - otherwise redundant
      dispatch({ type: LOGOUT_USER });
    }
  }, [dispatch]);

  // for navigation bar logic
  return (
    <div className="app-container">
      <Navbar />
      {props.children}
    </div>
  );
};
