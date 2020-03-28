import React from "react";
import styled from "styled-components";
import NestedComment from "./NestedComment";

const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-left: 2px black solid;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
  margin: 20px 0px;
`;

export default function CommentThread({ comment, handleCommentSubmit }) {
  return (
    <Display>
      <NestedComment parentList={[]} comment={comment} handleCommentSubmit={handleCommentSubmit} isRoot={true}></NestedComment>
    </Display>
  );
}
