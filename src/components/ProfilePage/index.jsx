import React, { useEffect, useState, useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { useLocation } from "react-router";
import { getPostsByUserUuid } from "../../actions/posts";
import { useDispatch, useSelector } from "react-redux";
import PostsPreviewList from "./PostsPreviewList";
import CommentsPreviewList from "./CommentsPreviewList";

const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-radius: 15px;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
`;

const Header = styled.div`
  border-bottom: 7px solid
    ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  padding-bottom: 10px;
  margin-bottom: 10px;
`;

const ButtonWrapper = styled.div`
  display: flex;
  justify-content: flex-start;
`;

const ProfileButton = styled.button`
  background-color: Transparent;
  border: none;
  cursor: pointer;
  outline: 0;
  padding: 5px 0px 5px 0px;
  margin: 5px 30px 5px 0px;
  font-size: 30px;
`;

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`;

const ProfilePage = () => {
  const [selectedPost, setSelectedPost] = useState(true);
  const posts = useSelector(state => state.posts);
  const theme = useContext(ThemeContext);
  const location = useLocation();
  const dispatch = useDispatch();

  const user_uuid = location.pathname.split("/").reverse()[0];

  useEffect(() => {
    const getPosts = async () => {
      try {
        dispatch(await getPostsByUserUuid(user_uuid));
      } catch (e) {
        console.log(e);
      }
    };

    getPosts();
  }, [getPostsByUserUuid, user_uuid]);

  const renderButtonsAndPosts = () => {
    if (selectedPost) {
      return (
        <div>
          <ButtonWrapper>
            <ProfileButton
              style={{ fontWeight: "bold" }}
              onClick={handlePostsClick}
            >
              Posts
            </ProfileButton>
            <ProfileButton
              style={{ fontWeight: "normal" }}
              onClick={handleCommentsClick}
            >
              Comments
            </ProfileButton>
          </ButtonWrapper>
          <PostsPreviewList posts={posts} />
        </div>
      );
    } else {
      return (
        <div>
          <ButtonWrapper>
            <ProfileButton
              style={{ fontWeight: "normal" }}
              onClick={handlePostsClick}
            >
              Posts
            </ProfileButton>
            <ProfileButton
              style={{ fontWeight: "bold" }}
              onClick={handleCommentsClick}
            >
              Comments
            </ProfileButton>
          </ButtonWrapper>
          <CommentsPreviewList />
        </div>
      );
    }
  };

  const handlePostsClick = () => {
    setSelectedPost(true);
  };

  const handleCommentsClick = () => {
    setSelectedPost(false);
  };

  return (
    <Wrapper>
      <Display theme={theme}>
        <Header>
          <h2>{user_uuid}</h2>
        </Header>
        {renderButtonsAndPosts()}
      </Display>
    </Wrapper>
  );
};

export default ProfilePage;
