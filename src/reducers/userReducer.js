import { LOGIN_USER, LOGOUT_USER } from "../actions/types";
import ls from "local-storage";

const userReducer = (state = null, action) => {
  switch (action.type) {
    case LOGIN_USER:
      // save to localstorage
      ls.set("user", action.user);
      return action.user;
    case LOGOUT_USER:
      ls.set("user", null);
      // remove from localstorage
      return null;
    default:
      return state;
  }
};

export default userReducer;
