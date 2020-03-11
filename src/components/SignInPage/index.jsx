import React from "React";
import SignInForm from "./SignInForm";
import { useDispatch } from "react-redux";
import { loginUser } from "../../actions/users";

const SignInPage = () => {
    const dispatch = useDispatch();
  // later write code to post to API
  const handleSignin = async (username, password) => {
    try {
      dispatch(await loginUser(username, password));
      // redirect
      history.push("/");
    } catch(error) {
      // error stuff
      console.log(error);
    }
  };
  return (
    <div>
      <SignInForm handleSubmit={handleSignin}></SignInForm>
    </div>
  );
};

export default SignInPage;