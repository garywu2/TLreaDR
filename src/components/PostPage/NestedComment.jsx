import React, { useState } from "react";
import styled from "styled-components";
import Comment from "./Comment";
import CommentForm from "./CommentForm";
import FormButton from "../styled/FormButton";

const Display = styled.div`
  display: flex;
  flex-direction: row;
  align-items: stretch;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  margin-top: 10px;
`;

const Thread = styled.div`
  flex: 1;
`;

const Bar = styled.div`
  width: 4px;
  background-color: gray;
  margin-right: 6px;
  border-radius: 2px;
`;

export default function NestedComment({
  comment,
  isRoot,
  handleCommentSubmit
}) {
  const [showReplyForm, setShowReplyForm] = useState(false);

  const handleReplyClick = () => {
    setShowReplyForm(!showReplyForm);
  };

  const handleReplySubmit = commentText => {
    const parentId = comment.id;
    // add parent uuid (this comment)
    handleCommentSubmit(commentText, parentId);
  };

  const renderChildrenComments = () => {
    return comment.nested_comment.map(com => (
      <NestedComment
        key={com.comment_uuid}
        comment={com}
        isRoot={false}
        handleCommentSubmit={handleCommentSubmit}
      ></NestedComment>
    ));
  };

  const renderReplyForm = () => {
    // comment form handlesubmit only passes in comment text as argument
    return (
      <CommentForm
        handleSubmit={handleReplySubmit}
        placeholder="Type your reply here..."
      ></CommentForm>
    );
  };

  return (
    <Display>
      {!isRoot && <Bar />}
      <Thread>
        <Comment
          comment={comment}
          handleReplyClick={handleReplyClick}
        ></Comment>
        {showReplyForm && renderReplyForm()}
        {renderChildrenComments()}
      </Thread>
    </Display>
  );
}
