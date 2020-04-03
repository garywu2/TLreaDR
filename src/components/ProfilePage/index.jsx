import React, { useEffect, useState, useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { useLocation } from "react-router";
import { getPostsByUserUuid } from "../../actions/posts";
import { getCommentsByUserUuid } from "../../actions/comments";
import { getUserFromUserUuid } from "../../actions/users";
import { getProfileFromUserUuid } from "../../actions/users";
import PostsPreviewList from "./PostsPreviewList";
import CommentsPreviewList from "./CommentsPreviewList";
import FormButton from "../styled/FormButton";
import { useHistory } from 'react-router-dom';
import { fetchProfile } from "../../actions/users";
import ProfilePreview from "./ProfilePreview";

const EditButton = styled(FormButton)`
  margin: 5px 0px;
  padding: 10px;
`;

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
  const [user, setUser] = useState(null);
  const [selectedPost, setSelectedPost] = useState("0");
  const [posts, setPosts] = useState(null);
  const [profile, setProfile] = useState(null);
  const [comments, setComments] = useState(null);
  const theme = useContext(ThemeContext);
  const location = useLocation();
  const history = useHistory();
  const user_uuid = location.pathname.split("/user/").reverse()[0];

  useEffect(() => {
    const getUsername = async () => {
      try {
        const { user } = await getUserFromUserUuid(user_uuid);
        setUser(user);
      } catch (e) {
        console.log(e);
      }
    };
    

    const getComments = async () => {
      try {
        const { comments } = await getCommentsByUserUuid(user_uuid);
        setComments(comments);
      } catch (e) {
        console.log(e);
      }
    };

    const getPosts = async () => {
      try {
        const { posts } = await getPostsByUserUuid(user_uuid);
        setPosts(posts);
      } catch (e) {
        console.log(e);
      }
    };

    const getProfile = async () => {
      try {
        const { profile } = await fetch(user_uuid);
        setProfile(profile);
      } catch (e) {
        console.log(e);
      }
    };

    getUsername();
    getPosts();
    getComments();
    getProfile();
  }, [
    getPostsByUserUuid,
    getCommentsByUserUuid,
    getUserFromUserUuid,
    getProfileFromUserUuid,
    user_uuid
  ]);

  const goToEditPage = () => {
    history.push("/user/edit/" + user_uuid);
  };

  const renderButtonsAndPosts = () => {
    if (selectedPost == "1") {
      return (
        <div>
          <ButtonWrapper>
            <ProfileButton 
              style={{fontWeight: "normal"}}
              onClick={handleProfileClick}
              >
                Profile
            </ProfileButton>
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
    } else if (selectedPost == "2"){
      return (
        <div>
          <ButtonWrapper>
            <ProfileButton 
              style={{fontWeight: "normal"}}
              onClick={handleProfileClick}
              >
                Profile
            </ProfileButton>
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
          <CommentsPreviewList comments={comments} username={user.username} />
        </div>
      );
    } else if(selectedPost == "0") {
      return (
        <div>
          <ButtonWrapper>
            <ProfileButton 
              style={{fontWeight: "bold"}}
              onClick={handleProfileClick}
              >
                Profile
            </ProfileButton>
            <ProfileButton
              style={{ fontWeight: "normal" }}
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
          <ProfilePreview profile={profile} ></ProfilePreview>
        </div>
      );
    }
  };

  const handlePostsClick = () => {
    setSelectedPost("1");
  };

  const handleCommentsClick = () => {
    setSelectedPost("2");
  };
  const handleProfileClick = () => {
    setSelectedPost("0");
  };

  return (
    <Wrapper>
      <Display theme={theme}>
        <Header>
          <h2>{user ? user.username : <div>Loading...</div>}</h2>
        </Header>
        <EditButton theme={theme} onClick={goToEditPage} >Edit Profilie</EditButton>
        {renderButtonsAndPosts()}
      </Display>
    </Wrapper>
  );
};

export default ProfilePage;
