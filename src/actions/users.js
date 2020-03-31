import axios from "axios";
import config from "../config/client";
import {FETCH_USERS, LOGIN_USER, FETCH_USER} from "./types";

export const addUser = async (email, username, password) => {
  const body = { email, username, password };

  // register user to database
  const response = await axios.post(config.endpoint + "users", { ...body });

  if(response.status !== 200) {
    throw "Registration failed with error code " + response.status;
  }

  // update store with user info if successfully registered
  return {type: LOGIN_USER, user: response.data}

};

export const loginUser = async (username, password) => {
  const body = { username, password };

  // register user to database
  const response = await axios.post(config.endpoint + "users/login", body);

  if(response.status !== 200) {
    throw "Login failed with error code " + response.status;
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

export const getUserFromUserUuid = async user_uuid => {
  const response = await axios.get(`${config.endpoint}users/${user_uuid}`);

  if (response.status !== 200) {
    throw "fetchUserFromUserUuid failed with error code " + response.status;
  }

  return { type: FETCH_USER, user: response.data };
}