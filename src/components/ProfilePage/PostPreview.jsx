import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

const PostPreviewWrapper = styled.div`
  background-color: #f5edf3;
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

const Img = styled.img`
  width: 100px;
  border-radius: 10px;
  margin: 10px;
`;

const PreviewBody = styled.div`
  display: flex;
  flex-direction: column;
  margin: 10px;
`;

const PreviewBodyTitle = styled(Link)`
  font-size: 25px;
  font-family: "Arvo", "sans-serif";
  margin-bottom: 10px;
`;

const PreviewBodySupplementary = styled.div`
  display: flex;
  font-size: 15px;
  font-family: "Montserrat", "sans-serif";
`;

const PostPreview = ({ post }) => {
  return (
    <PostPreviewWrapper>
      <Bar />
      <Img src={post.image_link} />
      <PreviewBody>
        <PreviewBodyTitle to={"/post/".concat(post.post_uuid)}>
          {post.title}
        </PreviewBodyTitle>
        <PreviewBodySupplementary>
          Posted by {post.author.username}
        </PreviewBodySupplementary>
      </PreviewBody>
    </PostPreviewWrapper>
  );
};

export default PostPreview;
