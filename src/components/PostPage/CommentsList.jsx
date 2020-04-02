import React from "react";
import styled from "styled-components";
import CommentThread from "./CommentThread";
import CommentForm from "./CommentForm";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

const Title = styled.h2`
  color: white;
  margin: 10px 0px;
`;

const SignInText = styled.div`
  color: white;
  text-align: center;
  width: 100%;
  margin: 10px auto;
`;

const SignInLink = styled(Link)`
  text-decoration: underline;
`;

export default function CommentsList({
  comments,
  handleCommentSubmit,
  handleEditSubmit,
  handleDelete
}) {
  const user = useSelector(state => state.user);

  const renderForm = () => {
    if (user) {
      return (
        <React.Fragment>
          <Title>Post a comment</Title>
          <CommentForm
            handleSubmit={commentText => handleCommentSubmit(commentText, [])}
            placeholder="Write a comment here..."
          ></CommentForm>
        </React.Fragment>
      );
    } else {
      return (
        <SignInText>
          <SignInLink to="/sign-in">Sign in</SignInLink> to post a comment!
        </SignInText>
      );
    }
  };

  return (
    <div>
      {renderForm()}
      {comments ? (
        <div>
          <Title>Comments</Title>
          {comments.map(comment => (
            <CommentThread
              key={comment.comment_uuid}
              handleCommentSubmit={handleCommentSubmit}
              handleEditSubmit={handleEditSubmit}
              handleDelete={handleDelete}
              comment={comment}
            ></CommentThread>
          ))}
        </div>
      ) : (
        "Loading..."
      )}
    </div>
  );
}
