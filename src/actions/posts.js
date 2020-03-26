import axios from "axios";
import config from "../config/client";
import { FETCH_POSTS, CLEAR_POSTS } from "./types";

export const getPostsByCategory = async categoryName => {
  const response = await axios.get(`${config.endpoint}${categoryName}/posts`);

  if (response.status !== 200) {
    throw "getPosts failed with error code " + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
};

export const getPostsBySearch = async (searchInput) => {
  const response = await axios.get(`${config.endpoint}all/search/${searchInput}`);

  if(response.status != 200) {
    throw "getPostsBySearch failed with error code" + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
}

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
