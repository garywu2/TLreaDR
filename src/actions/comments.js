import config from "../config/client";
import axios from "axios";
import { FETCH_COMMENTS, UPLOAD_COMMENTS } from "./types";

export const getCommentsByPostUuid = async post_uuid => {
  const response = await axios.get(`${config.endpoint}comments/${post_uuid}`);

  if (response.status !== 200) {
    throw "getPosts failed with error code " + response.status;
  }

  return { type: "GET_POST", comments: response.data };
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

  if (response.status !== 200) {
    throw "comment failed with error code " + response.status;
  }

  return { type: "POST_COMMENT", response: response.data };
};
