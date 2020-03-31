import React from "react";
import PostPreview from "./PostPreview";

const PostsPreviewList = ({ posts }) => {
  const renderPosts = posts => {
    if (!posts) {
      return <div>Loading posts...</div>;
    } else if (posts.length == 0) {
      return <div>No posts found.</div>;
    }

    return posts.map(post => <PostPreview key={post.post_uuid} post={post} />);
  };

  return <div>{renderPosts(posts)}</div>;
};

export default PostsPreviewList;
