import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPostByUuid } from "../../actions/posts";
import { getCommentsByPostUuid } from "../../actions/comments";
import PostInfo from "./PostInfo";
import CommentsList from "./CommentsList";
import styled from "styled-components";
import { useSelector } from "react-redux";
import { postComment } from "../../actions/comments";

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`;

const PostPage = props => {
  const location = useLocation();
  const user = useSelector(state => state.user);
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

  const insertComment = (newComment, parentList) => {
    // recursively find place to put comment

    // new comment doesn't have nestedComment attribute, add
    newComment.nested_comment = [];

    // shallow copy comments
    const newComments = [...comments];
    // nested_comment to conform to rest of nested comments
    let parent = { nested_comment: newComments };

    while (parentList.length) {
      const commentId = parentList.shift();

      parent = parent.nested_comment.find(comment => comment.id === commentId);
    }
    parent.nested_comment.push(newComment);

    setComments(newComments);
  };

  // commentText and parentUuid are from the comment at its level
  const handleCommentSubmit = async (commentText, parentList) => {
    const authorUuid = user.user_uuid;
    const postUuid = post.post_uuid;
    const parentId = parentList.length
      ? parentList[parentList.length - 1]
      : null;

    try {
      const { comment } = await postComment(
        commentText,
        authorUuid,
        postUuid,
        parentId
      );
      insertComment(comment, parentList);
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
