import React, { useState } from "react";
import NewPostForm from "./NewPostForm";
import PostPreview from "./PostPreview";
import { uploadPost } from "../../actions/posts";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";

const NewPostPage = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [hasErrors, setHasErrors] = useState(false);
  const user = useSelector(state => state.user);

  const [formValues, setFormValues] = useState({
    category: "",
    title: "",
    body: "",
    image_link: ""
  });

  // later write code to post to API
  const handleUpload = async () => {
    const { category, title, body, image_link } = formValues;

    try {
      const { postUuid } = await uploadPost(
        category,
        title,
        body,
        image_link,
        user.user_uuid
      );
      // redirect
      history.push("/post/" + postUuid);
    } catch (error) {
      console.log(error);
      setHasErrors(true);
    }
  };

  return (
    <div>
      <NewPostForm
        formValues={formValues}
        setFormValues={setFormValues}
        handleSubmit={handleUpload}
        hasErrors={hasErrors}
      ></NewPostForm>
      <PostPreview formValues={formValues}></PostPreview>
    </div>
  );
};

export default NewPostPage;
