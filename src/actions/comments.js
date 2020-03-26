import config from "../config/client";
import axios from "axios";
import { FETCH_COMMENTS, UPLOAD_COMMENTS } from "./types";

export const getCommentsByPostUuid = async post_uuid => {
  const response = await axios.get(`${config.endpoint}comments/${post_uuid}`);

  if(response.status !== 200) {
    throw "getPosts failed with error code " + response.status;
  }

  return { type: "GET_POST", comments: response.data };
};

export const uploadComment = async (comment) => {
  const params = { comment };

  // put comment into database
  const response = await axios.get(config.endpoint + "comment", {
    params
  });

  if(response.status !== 200) {
    throw "comment failed with error code " + response.status;
  }

  return {type: UPLOAD_COMMENTS, user: response.data}
};
