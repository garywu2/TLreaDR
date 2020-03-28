import React, { useState } from "react";
import SignInForm from "./SignInForm";
import { useDispatch } from "react-redux";
import { loginUser } from "../../actions/users";
import { useHistory } from "react-router-dom";

const SignInPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [hasErrors, setHasErrors] = useState(false);

  // later write code to post to API
  const handleSignin = async (username, password) => {
    try {
      dispatch(await loginUser(username, password));
      // redirect
      history.push("/category/all");
    } catch (error) {
      // error stuff
      setHasErrors(true);
      console.log(error);
    }
  };

  return (
    <div>
      <SignInForm handleSubmit={handleSignin} hasErrors={hasErrors}></SignInForm>
    </div>
  );
};

export default SignInPage;