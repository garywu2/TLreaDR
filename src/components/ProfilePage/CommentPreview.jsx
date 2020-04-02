import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";

const CommentPreviewWrapper = styled(Link)`
  background-color: #d5eef5;
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
`;

const Bar = styled.div`
  width: 8px;
  background-color: gray;
  margin-right: 6px;
  border-radius: 2px;
`;

const PreviewBody = styled.div`
  display: flex;
  flex-direction: column;
  margin: 10px;
`;

const PreviewBodyTitle = styled.div`
  font-size: 15px;
  font-family: "Montserrat", "sans-serif";
`;

const PreviewBodySupplementary = styled.div`
  display: flex;
  font-size: 25px;
  font-family: "Arvo", "sans-serif";
`;

const CommentPreview = ({ comment, username }) => {
  return (
    <CommentPreviewWrapper to={"/post/".concat(comment.post_uuid)}>
      <Bar />
      <PreviewBody>
        <PreviewBodyTitle>
          {username} commented on {convertDate(comment.date_submitted)}
        </PreviewBodyTitle>
        <PreviewBodySupplementary>
          {comment.comment_text}
        </PreviewBodySupplementary>
      </PreviewBody>
    </CommentPreviewWrapper>
  );
};

export default CommentPreview;
