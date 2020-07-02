import React, { useEffect, useState } from "react";
import { useLocation, useHistory } from "react-router-dom";
import { getPostByUuid, deletePost } from "../../actions/posts";
import {
  getCommentsByPostUuid,
  postComment,
  editComment,
  deleteComment
} from "../../actions/comments";
import PostInfo from "./PostInfo";
import CommentsList from "./CommentsList";
import styled from "styled-components";
import { useSelector } from "react-redux";
import { UPVOTE, DOWNVOTE } from "../../actions/types";

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`;

const PostPage = props => {
  const location = useLocation();
  const user = useSelector(state => state.user);
  const userLoaded = useSelector(state => state.loaded.userLoaded);
  const [post, setPost] = useState(null);
  const [hasErrors, setHasErrors] = useState(false);
  const [comments, setComments] = useState(null);
  const history = useHistory();
  const [commentRequestError, setCommentRequestError] = useState(false);

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
          setCommentRequestError(false);
        } catch (e) {
          const code = +e.message.split(" ").pop();
          if (code === 503) {
            setCommentRequestError(true);
          }
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

      comment = comment.nested_comment.find(
        comment => comment.id === commentId
      );
    }

    return comment;
  };

  const insertComment = (newComment, parentList) => {
    // recursively find place to put comment

    // new comment doesn't have nestedComment attribute, add
    newComment.nested_comment = [];

    // need this before pushing from array
    const parentListLength = parentList.length;

    // shallow copy comments
    const newComments = [...comments];
    let parent = findTargetComment(newComments, parentList);

    // if root comment, push to top
    if (parentListLength === 0) {
      parent.nested_comment.splice(0, 0, newComment);
    } else {
      parent.nested_comment.push(newComment);
    }

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

  const handleDeletePost = async () => {
    try {
      await deletePost(post.post_uuid);
      history.push("/");
    } catch (e) {
      console.log(e);
      setHasErrors(true);
    }
  };

  const editCommentInTree = (commentText, parentList) => {
    // recursively find place to put comment
    // shallow copy comments
    const newComments = [...comments];
    let comment = findTargetComment(newComments, parentList);

    comment.comment_text = commentText;
    comment.is_edited = true;
    comment.date_edited = new Date().toISOString();

    setComments(newComments);
  };

  const deleteCommentInTree = parentList => {
    // recursively find place to put comment
    // shallow copy comments
    const newComments = [...comments];
    let comment = findTargetComment(newComments, parentList);

    comment.is_deleted = true;

    setComments(newComments);
  };

  const handleEditSubmit = async (commentUuid, commentText, parentList) => {
    try {
      await editComment(commentText, commentUuid);
      // parentList to traverse - no commentUuid needed
      editCommentInTree(commentText, parentList);
    } catch (e) {
      console.log(e);
    }
  };

  const handleDeleteComment = async (commentUuid, parentList) => {
    try {
      await deleteComment(commentUuid);
      // parentList to traverse - no commentUuid needed
      deleteCommentInTree(parentList);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Wrapper>
      {post ? (
        <PostInfo
          post={post}
          votePost={votePost}
          handleDelete={handleDeletePost}
          hasErrors={hasErrors}
        ></PostInfo>
      ) : (
        <div>Loading...</div>
      )}
      {comments ? (
        <CommentsList
          comments={comments}
          handleCommentSubmit={handleCommentSubmit}
          handleEditSubmit={handleEditSubmit}
          handleDelete={handleDeleteComment}
        ></CommentsList>
      ) : commentRequestError ? (
        <div>The comment service is down.</div>
      ) : (
        <div>Loading...</div>
      )}
    </Wrapper>
  );
};

export default PostPage;
