import React, { useState } from "react";
import CreatePostForm from "./CreatePostForm";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";

const CreatePostPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [hasErrors, setHasErrors] = useState(false);

  // later write code to post to API
  const CreatePostForm = async (title, description) => {
    try {
      dispatch(await createPost(title, description));
      // redirect
      history.push("/");
    } catch (error) {
      // error stuff
      setHasErrors(true);
      console.log(error);
    }
  };

  return (
    <div>
      <CreatePostForm handleSubmit={handleSignin}></CreatePostForm>
    </div>
  );
};

export default CreatePostForm;