import axios from "axios";
import config from "../config/client";
import {
  FETCH_POSTS,
  CLEAR_POSTS,
  UPVOTE,
  DOWNVOTE,
  EDIT_POST,
  GET_POST,
  UPLOAD_POST,
  DELETE_POST
} from "./types";

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
    throw {
      message: "getPostsBySearch failed with error code" + response.status,
      status: response.status
    };
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
};

export const uploadPost = async (
  category,
  title,
  body,
  imageLink,
  articleLink,
  authorUuid
) => {
  const reqBody = {
    title,
    body,
    image_link: imageLink,
    article_link: articleLink,
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
  return { type: UPLOAD_POST, postUuid: post_uuid };
};

export const editPost = async (
  category,
  post_uuid,
  new_title,
  new_body,
  new_image_link,
  new_article_link
) => {
  const reqBody = {
    new_title,
    new_body,
    new_image_link,
    new_article_link
  };

  const response = await axios.put(
    `${config.endpoint}${category.toLowerCase()}/${post_uuid}`,
    reqBody
  );

  if (response.status !== 200) {
    console.log(response);
    throw "editPost failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  return { type: EDIT_POST };
};

export const deletePost = async post_uuid => {
  const response = await axios.delete(`${config.endpoint}all/${post_uuid}`);

  if (response.status !== 200) {
    throw "deletePost failed with the error code " + response.status;
  }

  return { type: DELETE_POST };
};

export const clearPosts = () => {
  return { type: CLEAR_POSTS };
};

export const getPostByUuid = async (postUuid, userUuid) => {
  let response;
  // if user is null, i.e., not logged in, don't pass params
  if (userUuid) {
    response = await axios.get(`${config.endpoint}all/${postUuid}`, {
      params: { user_uuid: userUuid }
    });
  } else {
    response = await axios.get(`${config.endpoint}all/${postUuid}`);
  }
  return { type: GET_POST, post: response.data };
};

export const getPostsByUserUuid = async user_uuid => {
  const response = await axios.get(`${config.endpoint}all/posts/${user_uuid}`);

  if (response.status !== 200) {
    throw "getPostsByUserUuid failed with the error code " + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
};

export const upvotePost = async (postUuid, userUuid, voteStatus) => {
  const body = {};

  // decide which HTTP request to make
  // if no upvotes, make a POST request
  // if upvoted, undo - DELETE request
  // if downvoted, edit - PUT request
  let axiosReqFunc;
  switch (voteStatus) {
    case null:
      axiosReqFunc = axios.post;
      body.vote_type = 1;
      body.user_uuid = userUuid;
      break;
    case 1:
      axiosReqFunc = axios.delete;
      body.data = { user_uuid: userUuid };
      break;
    case -1:
      axiosReqFunc = axios.put;
      body.user_uuid = userUuid;
      body.new_vote_type = 1;
      break;
    default:
      console.log("invalid vote_type: " + vote_type);
      return;
  }

  const response = await axiosReqFunc(
    `${config.endpoint}all/${postUuid}/vote`,
    body
  );

  if (response.status !== 201) {
    console.log(response);
    throw "upvote request failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  return { type: UPVOTE, oldVoteStatus: voteStatus, postUuid };
};

export const downvotePost = async (postUuid, userUuid, voteStatus) => {
  const body = {};

  // decide which HTTP request to make
  // if no upvotes, make a POST request
  // if downvoted, undo - DELETE request
  // if upvoted, edit - PUT request
  let axiosReqFunc;
  switch (voteStatus) {
    case null:
      axiosReqFunc = axios.post;
      body.vote_type = -1;
      body.user_uuid = userUuid;
      break;
    case -1:
      axiosReqFunc = axios.delete;
      body.data = { user_uuid: userUuid };
      break;
    case 1:
      axiosReqFunc = axios.put;
      body.user_uuid = userUuid;
      body.new_vote_type = -1;
      break;
    default:
      console.log("invalid vote_type: " + vote_type);
      return;
  }

  const response = await axiosReqFunc(
    `${config.endpoint}all/${postUuid}/vote`,
    body
  );

  if (response.status !== 201) {
    console.log(response);
    throw "upvote request failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  return { type: DOWNVOTE, oldVoteStatus: voteStatus, postUuid };
};

export const autoSummarizePost = async (articleLink) => {
  const body = {}
  let axiosReqFunc = axios.get
  body.article_link = articleLink
  const response = await axios.get(config.endpoint + "all/summarize", {
    params: body
  });

  if (response.status !== 200) {
    console.log(response);
    throw "summarize request failed with error code " +
      response.status +
      ": " +
      response.data.message;
  }

  return response.data;
}
