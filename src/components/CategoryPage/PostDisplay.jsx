import React, { useContext, useState } from "react";
import styled from "styled-components";
import PostExpanded from "./PostExpanded";
import PostPreview from "./PostPreview";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { upvotePost, downvotePost } from "../../actions/posts";

const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-radius: 15px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
`;

const Icons = styled.div`
  display: flex;
  flex-direction: column;
`;

const Icon = styled.div`
  color: #828282;
  cursor: pointer;
  margin-bottom: 10px;

  & :hover {
    color: ${({ hoverColor }) => hoverColor || "#131516"};
  }

  & > svg {
    transition: color 0.1s linear;
  }
`;

const Body = styled.div`
  flex: 1;
  margin: 0px 20px;
`;

const Header = styled.div`
  border-bottom: 7px solid
    ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  padding-bottom: 10px;
  margin-bottom: 10px;
`;

const Img = styled.img`
  width: 100%;
  object-fit: cover;
  max-height: 500px;
  padding-bottom: 10px;
  border-bottom: 7px solid
    ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  margin-bottom: 20px;
`;

export default function PostDisplay({ post }) {
  const [expanded, setExpanded] = useState(false);
  const user = useSelector(state => state.user);
  const history = useHistory();
  const dispatch = useDispatch();

  const handleExpand = () => {
    setExpanded(!expanded);
  };

  const handleThumbsUp = async () => {
    console.log("handle");
    if (user) {
      dispatch(
        await upvotePost(post.post_uuid, user.user_uuid, post.vote_type)
      );
    } else {
      history.push("/sign-in");
    }
  };

  const handleThumbsDown = async () => {
    if (user) {
      dispatch(
        await downvotePost(post.post_uuid, user.user_uuid, post.vote_type)
      );
    } else {
      history.push("/sign-in");
    }
  };

  return expanded ? (
    <PostExpanded
      post={post}
      handleExpand={handleExpand}
      handleThumbsUp={handleThumbsUp}
      handleThumbsDown={handleThumbsDown}
    />
  ) : (
    <PostPreview post={post} handleExpand={handleExpand} />
  );
}
