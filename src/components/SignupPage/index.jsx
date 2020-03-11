import React from "react";
import SignupForm from "./SignupForm";
import { fetchUsers, addUser, loginUser } from "../../actions/users";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";

const SignupPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();

  // later write code to post to API
  const handleSignup = async (email, username, password) => {
    try {
      dispatch(await addUser(email, username, password));
      // redirect
      history.push("/");
    } catch(error) {
      // error stuff
      console.log(error);
    }
  };

  return (
    <div>
      <SignupForm handleSubmit={handleSignup}></SignupForm>
    </div>
  );
};

export default SignupPage;
