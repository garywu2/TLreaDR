import { combineReducers } from "redux";
import userReducer from "./userReducer";
import postsReducer from "./postsReducer";
import categoriesReducer from "./categoriesReducer";
import { connectRouter } from "connected-react-router";
import loadedReducer from "./loadedReducer";

export const rootReducer = history =>
  combineReducers({
    user: userReducer,
    posts: postsReducer,
    categories: categoriesReducer,
    loaded: loadedReducer,
    router: connectRouter(history)
  });
