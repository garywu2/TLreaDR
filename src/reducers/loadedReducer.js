import { LOGIN_USER, LOGOUT_USER } from "../actions/types";

// verify intermediate loading states
const loadedReducer = (state = { userLoaded: false }, action) => {
  switch (action.type) {
    case LOGIN_USER:
      // save to localstorage
      return { ...state, userLoaded: true };
    case LOGOUT_USER:
      return { ...state, userLoaded: true };
    default:
      return state;
  }
};

export default loadedReducer;
