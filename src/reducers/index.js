import { combineReducers } from "redux";
import userReducer from "./userReducer";
import postsReducer from "./postsReducer";
import { connectRouter } from "connected-react-router";

export const rootReducer = history =>
  combineReducers({
    user: userReducer,
    posts: postsReducer,
    router: connectRouter(history)
  });
