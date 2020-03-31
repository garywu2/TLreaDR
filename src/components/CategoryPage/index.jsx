import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import { getPostsByCategory, upvotePost } from "../../actions/posts";
import PostsList from "./PostsList";

// custom hook (I'm trying it out lol)
const usePosts = () => {
  const dispatch = useDispatch();
  const posts = useSelector(state => state.posts);
  const user = useSelector(state => state.user);
  // obtains category from URL
  const location = useLocation();

  const categoryName = location.pathname.split("/").reverse()[0];

  let error = null;

  // grab posts on mount
  useEffect(() => {
    // this pattern is for async functions
    const getPosts = async () => {
      try {
        // if user is null, not logged in - pass null to action
        const userUuid = user ? user.user_uuid : null;
        console.log(userUuid);
        dispatch(await getPostsByCategory(categoryName, userUuid));
      } catch (e) {
        error = e;
      }
    };

    getPosts();
  }, [user, getPostsByCategory, categoryName, location]);

  return [posts, error];
};

const CategoryPage = props => {
  const [posts, error] = usePosts();

  return (
    <div>
      <PostsList posts={posts}></PostsList>
    </div>
  );
};

export default CategoryPage;
