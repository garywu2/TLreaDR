import config from "../config/client";
import axios from "axios";
import { FETCH_COMMENTS, POST_COMMENT, EDIT_COMMENT, DELETE_COMMENT } from "./types";

export const getCommentsByPostUuid = async post_uuid => {
  const response = await axios.get(`${config.endpoint}comments/${post_uuid}`);

  if (response.status !== 200) {
    throw "getPosts failed with error code " + response.status;
  }

  return { type: FETCH_COMMENTS, comments: response.data };
};

export const postComment = async (
  commentText,
  authorUuid,
  postUuid,
  parentId
) => {
  const body = {
    text: commentText,
    author_uuid: authorUuid,
    post_uuid: postUuid
  };
  if (parentId) {
    body.parent_id = parentId;
  }

  // put comment into database
  const response = await axios.post(config.endpoint + "comments", body);

  if (response.status !== 201) {
    throw "comment failed with error code " + response.status;
  }

  return { type: POST_COMMENT, comment: response.data };
};

export const editComment = async (commentText, commentUuid) => {
  const body = { new_text: commentText };

  const response = await axios.put(
    config.endpoint + "comments/" + commentUuid,
    body
  );

  if (response.status !== 201) {
    throw "comment failed with error code " + response.status;
  }

  return { type: EDIT_COMMENT };
};

export const deleteComment = async (commentUuid) => {
  const response = await axios.delete(
    config.endpoint + "comments/" + commentUuid
  );

  if (response.status !== 200) {
    throw "comment failed with error code " + response.status;
  }

  return { type: DELETE_COMMENT };
};
