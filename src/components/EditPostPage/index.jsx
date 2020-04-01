import React, { useState, useEffect } from "react";
import EditPostForm from "./EditPostForm";
import PostPreview from "../NewPostPage/PostPreview";
import { editPost } from "../../actions/posts";
import { useHistory, useLocation } from "react-router-dom";

const EditPostPage = () => {
  const history = useHistory();
  const [hasErrors, setHasErrors] = useState(false);
  const location = useLocation();

  const post_uuid = location.pathname.split("/")[2];

  const [formValues, setFormValues] = useState({
    category: "",
    title: "",
    body: "",
    image_link: ""
  });

  const handleEdit = async () => {
    const { category, title, body, image_link } = formValues;

    try {
      await editPost(category, post_uuid, title, body, image_link);
      history.push("/post/" + post_uuid);
    } catch (error) {
      console.log(error);
      setHasErrors(true);
    }
  };

  const renderForm = () => {
    return (
      <div>
        <EditPostForm
          formValues={formValues}
          setFormValues={setFormValues}
          handleSubmit={handleEdit}
          hasErrors={hasErrors}
        ></EditPostForm>
        <PostPreview formValues={formValues}></PostPreview>
      </div>
    );
  };

  return <div>{renderForm()}</div>;
};

export default EditPostPage;
