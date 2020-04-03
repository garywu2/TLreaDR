import axios from "axios";
import config from "../config/client";
import {FETCH_USERS, LOGIN_USER, FETCH_USER, UPLOAD_PROFILE, GET_PROFILE} from "./types";

export const addUser = async (email, username, password, isAdmin) => {
  const body = { email, username, password, is_admin: +isAdmin };

  // register user to database
  const response = await axios.post(config.endpoint + "users", { ...body });

  if (response.status !== 200) {
    throw "Registration failed with error code " + response.status;
  }

  // update store with user info if successfully registered
  return { type: LOGIN_USER, user: response.data };
};

export const loginUser = async (username, password) => {
  const body = { username, password };

  // register user to database
  const response = await axios.get(config.endpoint + "users/login", {
    params: body
  });

  if (response.status !== 200) {
    throw "Login failed with error code " + response.status;
  }

  return { type: LOGIN_USER, user: response.data };
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

export const fetchProfile = async (user_uuid) => {
  const response = await axios.get(config.endpoint + "users/" + user_uuid);

  if (response.status !== 200) {
    console.log(e);
  }
  return {
    type: GET_PROFILE,
    user: response.data
  };
};

export const getProfileFromUserUuid = async (
  user_uuid,
  new_email,
  new_username,
  new_password,
) => {
  const reqBody = {
    new_email,
    new_username,
    new_password,
  };

  const response = await axios.put(`${config.endpoint}users/${user_uuid}`, reqBody);

  if (response.status !== 200) {
    throw "Registration failed with error code " + response.status;
  }

  return { type: UPLOAD_PROFILE, user: response.data };
};