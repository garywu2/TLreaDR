import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPostByUuid } from "../../actions/posts";
import { getCommentsByPostUuid } from "../../actions/comments";
import PostInfo from "./PostInfo";
import CommentsList from "./CommentsList";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import { postComment } from "../../actions/comments";

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`;

const PostPage = props => {
  const location = useLocation();
  const user = useSelector(state => state.user);
  const userUuid = user ? user.user_uuid : null;
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

  const insertComment = newComment => {
    console.log(newComment);
  };

  // commentText and parentUuid are from the comment at its level
  const handleCommentSubmit = async (commentText, parentId) => {
    const authorUuid = user.user_uuid;
    const postUuid = post.post_uuid;

    try {
      const { comment } = await postComment(
        commentText,
        authorUuid,
        postUuid,
        parentId
      );
      // probably don't dispatch - doesn't need to be global state
      insertComment(comment);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Wrapper>
      {post ? <PostInfo post={post}></PostInfo> : <div>Loading...</div>}
      {comments ? (
        <CommentsList
          comments={comments}
          handleCommentSubmit={handleCommentSubmit}
        ></CommentsList>
      ) : (
        <div>Loading...</div>
      )}
    </Wrapper>
  );
};

export default PostPage;
