import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import { getPostsBySearch } from "../../actions/posts";
import PostsList from "../CategoryPage/PostsList";

const usePosts = () => {
  const dispatch = useDispatch();
  const posts = useSelector(state => state.posts);
  const location = useLocation();

  const searchInput = location.pathname.split("/").reverse()[0].replace("%20"," ");


  useEffect(() => {
    const getPosts = async () => {
      try {
        dispatch(await getPostsBySearch(searchInput));
      } catch (e) {
        console.log(e);
      }
    };

    getPosts();
  }, [getPostsBySearch, searchInput, location]);

  return posts;
};

const SearchResultsPage = () => {
  const posts = usePosts();

  return (
    <div>
      <PostsList posts={posts}></PostsList>
    </div>
  );
};

export default SearchResultsPage;