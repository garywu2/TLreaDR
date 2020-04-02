import React, { useState, useEffect } from "react";
import EditPostForm from "./EditPostForm";
import PostPreview from "../NewPostPage/PostPreview";
import { editPost, getPostByUuid } from "../../actions/posts";
import { useHistory, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";

const EditPostPage = () => {
  const history = useHistory();
  const [hasErrors, setHasErrors] = useState(false);
  const [postAuthor, setPostAuthor] = useState(null);
  const user = useSelector(state => state.user);
  const location = useLocation();

  const post_uuid = location.pathname.split("/")[2];

  const [formValues, setFormValues] = useState({
    category: "",
    title: "",
    body: "",
    image_link: ""
  });

  useEffect(() => {
    const getPostInformation = async () => {
      try {
        const user_uuid = user ? user.user_uuid : null;
        const { post } = await getPostByUuid(post_uuid, user_uuid);
        setPostAuthor(post.author_uuid);
        setFormValues({
          category: post.category,
          title: post.title,
          body: post.body,
          image_link: post.image_link
        });
      } catch (e) {
        console.log(e);
      }
    };

    getPostInformation();
  }, [getPostByUuid, post_uuid]);

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

  return <div>{user && user.user_uuid == postAuthor && renderForm()}</div>;
};

export default EditPostPage;
