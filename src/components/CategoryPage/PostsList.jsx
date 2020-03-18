import React from "react";
import PostDisplay from "./PostDisplay";
import styled from 'styled-components';

const ListWrapper = styled.div`
  margin: 20px 0px;
  & > * {
    margin-bottom: 15px;
  }
`

export default function PostsList({ posts }) {
  const renderPosts = () => {
    if (!posts) {
      return <div>Loading...</div>;
    }
    return posts.map(post => (
      <PostDisplay key={post.post_uuid} post={post}></PostDisplay>
    ));
  };

  return <ListWrapper>{renderPosts()}</ListWrapper>;
}
