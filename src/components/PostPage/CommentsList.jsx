import React from "react";
import styled from "styled-components";
import Comment from "./Comment";

const Title = styled.h2`
  color: white;
  margin: 10px 0px;
`;

export default function CommentsList({ comments }) {
  console.log(comments);

  return (
    <div>
      {comments ? (
        <div>
          <Title>Comments</Title>
          {comments.map(comment => (
            <Comment key={comment.comment_uuid} comment={comment}></Comment>
          ))}
        </div>
      ) : (
        "Loading..."
      )}
    </div>
  );
}
