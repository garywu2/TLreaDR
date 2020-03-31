import { FETCH_POSTS, CLEAR_POSTS, UPVOTE, DOWNVOTE } from "../actions/types";

const postsReducer = (state = null, action) => {
  switch (action.type) {
    case FETCH_POSTS:
      return action.posts;
    case CLEAR_POSTS:
      return null;
    case UPVOTE: {
      const newState = state.map(post => {
        if (post.post_uuid === action.postUuid) {
          let newVotes, newVoteType;
          switch (action.oldVoteStatus) {
            case 1:
              // undo upvote
              newVotes = post.votes - 1;
              newVoteType = null;
              break;
            case -1:
              // turn downvote into upvote - plus 2
              newVotes = post.votes + 2;
              newVoteType = 1;
              break;
            case null:
              // turn nothing into upvote - plus 1
              newVotes = post.votes + 1;
              newVoteType = 1;
              break;
            default:
              console.log("Bad logic: oldVoteStatus is ", action.oldVoteStatus);
          }

          return {
            ...post,
            vote_type: newVoteType,
            // remove if de-upvoting, add if upvoting
            votes: newVotes
          };
        }
        return post;
      });

      return newState;
    }
    case DOWNVOTE: {
      const newState = state.map(post => {
        if (post.post_uuid === action.postUuid) {
          let newVotes, newVoteType;
          switch (action.oldVoteStatus) {
            case -1:
              // undo downvote
              newVotes = post.votes + 1;
              newVoteType = null;
              break;
            case 1:
              // turn upvote into downvote - minus 2
              newVotes = post.votes - 2;
              newVoteType = -1;
              break;
            case null:
              // turn nothing into downvote - minus 1
              newVotes = post.votes - 1;
              newVoteType = -1;
              break;
            default:
              console.log("Bad logic: oldVoteStatus is ", action.oldVoteStatus);
          }

          return {
            ...post,
            vote_type: newVoteType,
            // remove (add) if de-downvote, sutract if downvoting
            votes: newVotes
          };
        }
        return post;
      });

      return newState;
    }
    default:
      return state;
  }
};

export default postsReducer;
