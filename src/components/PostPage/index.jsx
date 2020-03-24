import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPostByUuid } from "../../actions/posts";
import { getCommentsByPostUuid } from "../../actions/comments";
import PostInfo from "./PostInfo";

// custom hook (I'm trying it out lol)
const usePost = () => {
  // obtains post uuid from URL
  const location = useLocation();

  let error = null;

  // grab posts on mount
  useEffect(() => {
    // this pattern is for async functions
    const getPosts = async () => {
      try {
        dispatch(await getPostsByCategory(categoryName));
      } catch (e) {
        error = e;
      }
    };

    getPosts();
  }, [getPostsByCategory, categoryName, location]);
};

const PostPage = props => {
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState(null);

  useEffect(() => {
    const getPost = async () => {
      try {
        const postUuid = location.pathname.split("/").reverse()[0];
        const { post } = await getPostByUuid(postUuid);
        setPost(post);
      } catch (e) {
        console.log(e);
      }
    };

    getPost();
  }, [setPost, getPostByUuid, location]);

  useEffect(() => {
    const getComments = async () => {
      if (post) {
        try {
          const { comments } = await getCommentsByPostUuid(post.post_uuid);
          setComments(comments);
        } catch (e) {
          console.log(e);
        }
      }
    };

    getComments();
  }, [post, getCommentsByPostUuid, setComments]);

  console.log(post, comments);

  return (
    <div>
      {post ? <PostInfo post={post}></PostInfo> : <div>Loading...</div>}
    </div>
  );
};

export default PostPage;
