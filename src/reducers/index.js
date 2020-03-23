import { combineReducers } from "redux";
import userReducer from "./userReducer";
import postsReducer from "./postsReducer";
import categoriesReducer from "./categoriesReducer";
import { connectRouter } from "connected-react-router";

export const rootReducer = history =>
  combineReducers({
    user: userReducer,
    posts: postsReducer,
    categories: categoriesReducer,
    router: connectRouter(history)
  });
