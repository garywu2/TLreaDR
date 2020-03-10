import { combineReducers } from "redux";
import userReducer from "./userReducer";
import { connectRouter } from "connected-react-router";

export const rootReducer = history =>
  combineReducers({
    user: userReducer,
    router: connectRouter(history)
  });
