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

export const getPostsBySearch = async (categoryName, searchInput) => {
  const response = await axios.get(`${config.endpoint}${categoryName}/${searchInput}`);

  if(response.status != 200) {
    throw "getPostsBySearch failed with error code" + response.status;
  }

  const { posts } = response.data;

  return { type: FETCH_POSTS, posts };
}