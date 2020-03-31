import React from "react";
import CommentPreview from "./CommentPreview";

const CommentsPreviewList = ({ comments, username }) => {
  const renderComments = comments => {
    if (!comments) {
      return <div>Loading comments...</div>;
    } else if (comments.length == 0) {
      return <div>No comments found.</div>;
    }

    return comments.map(comment => (
      <CommentPreview
        key={comment.comment_uuid}
        comment={comment}
        username={username}
      />
    ));
  };

  return <div>{renderComments(comments)}</div>;
};

export default CommentsPreviewList;
