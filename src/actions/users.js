import axios from "axios";
import config from "../config/client";
import {FETCH_USERS, LOGIN_USER} from "./types";

export const addUser = async (email, username, password) => {
  const body = { email, username, password };

  console.log(body);

  // register user to database
  const response = await axios.post(config.endpoint + "users", { ...body });

  // return true if successfully created
  if(response.status !== 201) {
    throw "Registration failed";
  }
};

export const loginUser = async (username, password) => {
  const params = { username, password };

  // register user to database
  const response = await axios.get(config.endpoint + "users/login", {
    params
  });

  if(response.status !== 200) {
    throw "Login failed";
  }

  return {type: LOGIN_USER, user: response.data}
};

export const fetchUsers = async () => {
  // config.endpoint
  const response = await axios.get(config.endpoint + "users");

  return {
    type: FETCH_USERS,
    users: response.data
  };
};