import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPostByUuid } from "../../actions/posts";
import { getCommentsByPostUuid } from "../../actions/comments";
import PostInfo from "./PostInfo";
import CommentsList from "./CommentsList";
import styled from "styled-components";
import { useSelector } from "react-redux";
import { postComment } from "../../actions/comments";
import { UPVOTE, DOWNVOTE } from "../../actions/types";

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`;

const PostPage = props => {
  const location = useLocation();
  const user = useSelector(state => state.user);
  const userLoaded = useSelector(state => state.loaded.userLoaded);
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState(null);

  useEffect(() => {
    const getPost = async () => {
      try {
        const postUuid = location.pathname.split("/").reverse()[0];
        const userUuid = user ? user.user_uuid : null;
        const { post } = await getPostByUuid(postUuid, userUuid);
        setPost(post);
      } catch (e) {
        console.log(e);
      }
    };

    if (userLoaded) {
      getPost();
    }
  }, [userLoaded, setPost, getPostByUuid, location]);

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

  // pesudo-reducer for updating the post
  const votePost = action => {
    switch (action.type) {
      case UPVOTE: {
        let newVotes, newVoteType;
        switch (action.oldVoteStatus) {
          case 1:
            // undo upvote
            newVotes = post.votes - 1;
            newVoteType = null;
            break;
          case -1:
            // turn downvote into upvote - plus 2
            newVotes = post.votes + 2;
            newVoteType = 1;
            break;
          case null:
            // turn nothing into upvote - plus 1
            newVotes = post.votes + 1;
            newVoteType = 1;
            break;
          default:
            console.log("Bad logic: oldVoteStatus is ", action.oldVoteStatus);
        }

        const updatedPost = {
          ...post,
          vote_type: newVoteType,
          // remove if de-upvoting, add if upvoting
          votes: newVotes
        };

        return setPost(updatedPost);
      }
      case DOWNVOTE: {
        let newVotes, newVoteType;
        switch (action.oldVoteStatus) {
          case -1:
            // undo downvote
            newVotes = post.votes + 1;
            newVoteType = null;
            break;
          case 1:
            // turn upvote into downvote - minus 2
            newVotes = post.votes - 2;
            newVoteType = -1;
            break;
          case null:
            // turn nothing into downvote - minus 1
            newVotes = post.votes - 1;
            newVoteType = -1;
            break;
          default:
            console.log("Bad logic: oldVoteStatus is ", action.oldVoteStatus);
        }

        const updatedPost = {
          ...post,
          vote_type: newVoteType,
          // remove (add) if de-downvote, sutract if downvoting
          votes: newVotes
        };

        return setPost(updatedPost);
      }
    }
  };

  const findTargetComment = (commentTree, parentList) => {
    // original response is an array - make fake root node
    // nested_comment to conform to rest of nested comments
    let comment = { nested_comment: commentTree };

    while (parentList.length) {
      const commentId = parentList.shift();

      comment = comment.nested_comment.find(comment => comment.id === commentId);
    }

    return comment;
  };

  const insertComment = (newComment, parentList) => {
    // recursively find place to put comment

    // new comment doesn't have nestedComment attribute, add
    newComment.nested_comment = [];

    // shallow copy comments
    const newComments = [...comments];
    // nested_comment to conform to rest of nested comments
    let parent = findTargetComment(newComments, parentList);

    parent.nested_comment.push(newComment);

    setComments(newComments);
  };

  // commentText and parentUuid are from the comment at its level
  const handleCommentSubmit = async (commentText, parentList) => {
    const authorUuid = user.user_uuid;
    const postUuid = post.post_uuid;
    const parentId = parentList.length
      ? parentList[parentList.length - 1]
      : null;

    try {
      const { comment } = await postComment(
        commentText,
        authorUuid,
        postUuid,
        parentId
      );
      insertComment(comment, parentList);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Wrapper>
      {post ? (
        <PostInfo post={post} votePost={votePost}></PostInfo>
      ) : (
        <div>Loading...</div>
      )}
      {comments ? (
        <CommentsList
          comments={comments}
          handleCommentSubmit={handleCommentSubmit}
        ></CommentsList>
      ) : (
        <div>Loading...</div>
      )}
    </Wrapper>
  );
};

export default PostPage;
