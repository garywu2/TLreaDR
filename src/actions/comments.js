import config from "../config/client";
import axios from "axios";

export const getCommentsByPostUuid = async post_uuid => {
  const response = await axios.get(`${config.endpoint}comments/${post_uuid}`);
  return { type: "GET_POST", comments: response.data };
};
