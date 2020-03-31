import axios from "axios";
import config from "../config/client";
import { FETCH_POSTS, CLEAR_POSTS } from "./types";

export const getPostsByCategory = async (categoryName, userUuid) => {
  let response;
  // if user is null, i.e., not logged in, don't pass params
  if (userUuid) {
    response = await axios.get(`${config.endpoint}${categoryName}/posts`, {
      params: { user_uuid: userUuid }
    });
  } else {
    response = await axios.get(`${config.endpoint}${categoryName}/posts`);
  }

  if (response.status !== 200) {
    throw "getPosts failed with error code " + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
};

export const getPostsBySearch = async searchInput => {
  const response = await axios.get(
    `${config.endpoint}all/search/${searchInput}`
  );

  if (response.status != 200) {
    throw "getPostsBySearch failed with error code" + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
};

export const uploadPost = async (
  category,
  title,
  body,
  imageLink,
  authorUuid
) => {
  const reqBody = {
    title,
    body,
    image_link: imageLink,
    author_uuid: authorUuid
  };

  const response = await axios.post(
    `${config.endpoint}${category.toLowerCase()}/posts`,
    reqBody
  );

  if (response.status !== 200) {
    console.log(response);
    throw "getPosts failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  const { post_uuid } = response.data;
  return { type: "UPLOAD_POST", postUuid: post_uuid };
};

export const getPostByUuid = async post_uuid => {
  const response = await axios.get(`${config.endpoint}all/${post_uuid}`);
  return { type: "GET_POST", post: response.data };
};

export const handleUpvote = async (
  postUuid,
  categoryName,
  userUuid,
  voteStatus
) => {
  body = { user_uuid: userUuid };

  // decide which HTTP request to make
  // if no upvotes, make a POST request
  // if downvoted, edit - PUT request
  // if upvoted, undo - DELETE request
  let axiosReqFunc;
  switch (voteStatus) {
    case null:
      func = axios.get;
      break;
    case 1:
      func = axios.delete;
    case -1:
      func = axios.put;
  }

  const response = await axiosReqFunc(
    `${config.endpoint}${categoryName}/${postUuid}/vote`,
    body
  );

  if (response.status !== 200) {
    console.log(response);
    throw "upvote request failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  return { type: "UPVOTE" };
};
