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

const ReplyHeader = styled.h3`
  margin-top: 10px;
`;

export default function NestedComment({
  comment,
  isRoot,
  handleCommentSubmit,
  handleEditSubmit,
  handleDelete,
  parentList
}) {
  const [showReplyForm, setShowReplyForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  // add this comment's id to the parent list
  const newParentList = [...parentList, comment.id];

  const handleReplyClick = () => {
    setShowReplyForm(!showReplyForm);
    setShowEditForm(false);
  };

  const handleEditClick = () => {
    setShowReplyForm(false);
    setShowEditForm(!showEditForm);
  };

  const handleDeleteClick = () => {
    handleDelete(comment.comment_uuid, newParentList);
  };

  const handleReplySubmit = async commentText => {
    await handleCommentSubmit(commentText, newParentList);
    // wait for comment to be posted
    setShowReplyForm(!showReplyForm);
  };

  const handleEditFormSubmit = async commentText => {
    await handleEditSubmit(comment.comment_uuid, commentText, newParentList);
    // wait for comment to be posted
    setShowEditForm(!showEditForm);
  };

  const renderChildrenComments = () => {
    return comment.nested_comment.map(com => (
      <NestedComment
        parentList={newParentList}
        key={com.comment_uuid}
        comment={com}
        isRoot={false}
        handleCommentSubmit={handleCommentSubmit}
        handleEditSubmit={handleEditSubmit}
        handleDelete={handleDelete}
      ></NestedComment>
    ));
  };

  const renderReplyForm = () => (
    // comment form handlesubmit only passes in comment text as argument
    <React.Fragment>
      <ReplyHeader>Reply to comment</ReplyHeader>
      <CommentForm
        handleSubmit={handleReplySubmit}
        placeholder="Type your reply here..."
      ></CommentForm>
    </React.Fragment>
  );

  const renderEditForm = () => (
    <React.Fragment>
      <ReplyHeader>Edit comment</ReplyHeader>
      <CommentForm
        handleSubmit={handleEditFormSubmit}
        value={comment.comment_text}
      ></CommentForm>
    </React.Fragment>
  );

  return (
    <Display>
      {!isRoot && <Bar />}
      <Thread>
        <Comment
          comment={comment}
          handleReplyClick={handleReplyClick}
          handleEditClick={handleEditClick}
          handleDeleteClick={handleDeleteClick}
          handleEditSubmit={handleEditSubmit}
        ></Comment>
        {showEditForm && renderEditForm()}
        {showReplyForm && renderReplyForm()}
        {renderChildrenComments()}
      </Thread>
    </Display>
  );
}
