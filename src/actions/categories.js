import axios from "axios";
import config from "../config/client";
import { FETCH_CATEGORIES, ADD_CATEGORY, DELETE_CATEGORY } from "./types";

export const getCategories = async () => {
  const response = await axios.get(`${config.endpoint}categories`);

  if (response.status != 200) {
    throw "Category retrieval failed with error code " + response.status;
  }

  return { type: FETCH_CATEGORIES, categories: response.data };
};

export const addCategory = async categoryName => {
  const body = { name: categoryName };

  const response = await axios.post(config.endpoint + "categories", body);

  if (response.status != 200) {
    throw "Category addition failed with error code " + response.status;
  }

  return { type: ADD_CATEGORY, category: response.data };
};

export const deleteCategory = async categoryName => {
  const response = await axios.delete(
    config.endpoint + "categories/" + categoryName
  );

  if (response.status != 201) {
    throw "Category addition failed with error code " + response.status;
  }

  return { type: DELETE_CATEGORY, categoryName };
};
