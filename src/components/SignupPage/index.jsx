import React, { useState } from "react";
import SignupForm from "./SignupForm";
import { addUser } from "../../actions/users";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";

const SignupPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [hasErrors, setHasErrors] = useState(false);

  // later write code to post to API
  const handleSignup = async (email, username, password) => {
    try {
      dispatch(await addUser(email, username, password));
      // redirect
      history.push("/");
    } catch (error) {
      console.log(error);
      setHasErrors(true);
    }
  };

  return (
    <div>
      <SignupForm
        handleSubmit={handleSignup}
        hasErrors={hasErrors}
      ></SignupForm>
    </div>
  );
};

export default SignupPage;
