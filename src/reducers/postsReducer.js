import { FETCH_POSTS, CLEAR_POSTS } from "../actions/types";

const postsReducer = (state = null, action) => {
  switch (action.type) {
    case FETCH_POSTS:
      return action.posts;
    case CLEAR_POSTS:
      return null;
    default:
      return state;
  }
};

export default postsReducer;