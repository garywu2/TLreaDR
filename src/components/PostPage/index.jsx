import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPostByUuid } from "../../actions/posts";
import { getCommentsByPostUuid } from "../../actions/comments";
import PostInfo from "./PostInfo";
import CommentsList from "./CommentsList";
import styled from 'styled-components';

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`

const PostPage = props => {
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState(null);

  useEffect(() => {
    const getPost = async () => {
      try {
        const postUuid = location.pathname.split("/").reverse()[0];
        const { post } = await getPostByUuid(postUuid);
        setPost(post);
      } catch (e) {
        console.log(e);
      }
    };

    getPost();
  }, [setPost, getPostByUuid, location]);

  useEffect(() => {
    const getComments = async () => {
      if (post) {
        try {
          const { comments } = await getCommentsByPostUuid(post.post_uuid);
          setComments(comments);
        } catch (e) {
          console.log(e);
        }
      }
    };

    getComments();
  }, [post, getCommentsByPostUuid, setComments]);

  console.log(post, comments);

  return (
    <Wrapper>
      {post ? <PostInfo post={post}></PostInfo> : <div>Loading...</div>}
      {comments ? (
        <CommentsList comments={comments}></CommentsList>
      ) : (
        <div>Loading...</div>
      )}
    </Wrapper>
  );
};

export default PostPage;
