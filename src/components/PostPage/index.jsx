import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import { getPostsByCategory } from "../../actions/posts";
import PostsList from "./PostsList";

// custom hook (I'm trying it out lol)
const usePosts = () => {
  const dispatch = useDispatch();
  const posts = useSelector(state => state.posts);
  // obtains category from URL
  const location = useLocation();

  const categoryName = location.pathname.split("/").reverse()[0];

  let error = null;

  // grab posts on mount
  useEffect(() => {
    // this pattern is for async functions
    const getPosts = async () => {
      try {
        dispatch(await getPostsByCategory(categoryName));
      } catch (e) {
        error = e;
      }
    };

    getPosts();
  }, [getPostsByCategory, categoryName, location]);

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
