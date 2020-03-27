import React from "react";
import styled from "styled-components";
import CommentThread from "./CommentThread";
import CommentForm from "./CommentForm";

const Title = styled.h2`
  color: white;
  margin: 10px 0px;
`;

export default function CommentsList({ comments, handleCommentSubmit }) {

  return (
    <div>
      <Title>Post a comment</Title>
      <CommentForm
        handleSubmit={handleCommentSubmit}
        placeholder="Write a comment here..."
      ></CommentForm>
      {comments ? (
        <div>
          <Title>Comments</Title>
          {comments.map(comment => (
            <CommentThread
              key={comment.comment_uuid}
              handleCommentSubmit={handleCommentSubmit}
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
