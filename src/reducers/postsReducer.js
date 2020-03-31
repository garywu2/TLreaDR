import { FETCH_POSTS, CLEAR_POSTS, UPVOTE } from "../actions/types";

const postsReducer = (state = null, action) => {
  switch (action.type) {
    case FETCH_POSTS:
      return action.posts;
    case CLEAR_POSTS:
      return null;
    case UPVOTE:
      const newState = state.map(post => {
        if (post.post_uuid === action.postUuid) {
          return {
            ...post,
            vote_type: action.voteStatus,
            // remove if de-upvoting, add if upvoting
            votes: post.votes + (action.voteStatus === 1 ? 1 : -1)
          };
        }
        return post;
      });

      return newState;
    default:
      return state;
  }
};

export default postsReducer;
