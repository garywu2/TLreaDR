import React, { useContext, useState } from "react";
import { useLocation } from "react-router-dom";
import styled, { ThemeContext } from "styled-components";
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

const ProfileDisplay = () => {
  const [selectedPost, setSelectedPost] = useState(true);
  const location = useLocation();
  const theme = useContext(ThemeContext);

  const userName = location.pathname.split("/").reverse()[0];

  const handlePostsClick = () => {
    setSelectedPost(true);
  };

  const handleCommentsClick = () => {
    setSelectedPost(false);
  };

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
          <PostsPreviewList />
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

  return (
    <Display theme={theme}>
      <Header>
        <h2>{userName}</h2>
      </Header>
      {renderButtonsAndPosts()}
    </Display>
  );
};

export default ProfileDisplay;
