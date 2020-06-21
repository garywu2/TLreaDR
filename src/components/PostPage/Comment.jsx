import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";
import { useSelector } from "react-redux";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faThumbsDown, faThumbsUp} from "@fortawesome/free-regular-svg-icons";

const Wrapper = styled.div`
  background-color: #e9e9e9;
  border-radius: 8px;
`;

const Body = styled.div`
  padding: 10px;
`;

const Header = styled.div``;

const Text = styled.p`
  padding: 10px;
`;

const BottomBar = styled.div`
  background-color: #c9c9c9;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 2rem;
`;

const RightSide = styled.div`
  display: flex;
  padding: 0 10px;
  align-items: center;
`;

const Icon = styled.div`
  color: #828282;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;

  & :hover {
    color: ${({ hoverColor }) => hoverColor || "#131516"};
  }

  & > svg {
    transition: color 0.1s linear;
  }
`;
const BottomBarButton = styled.button`
  border-radius: 4px;
  padding: 4px 8px;
  color: ${({ theme }) => (theme ? theme.secondaryTextColor : "#fff")};
  background-color: #c9c9c9;
  transition: background-color 0.1s linear;
  cursor: pointer;
  border: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};

  &:hover {
    background-color: #898989;
  }
`;

const Icons = styled.div`
  display: flex;
  flex-direction: row;
`;

const Points = styled.div`
  color: ${({ points }) => (points < 0 ? "red" : "black")};
  text-align: center;
  margin: 10px 0px;
  font-weight: bold;
  font-family: Arvo, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
`;

export default function Comment({
  comment,
  handleEditClick,
  handleDeleteClick,
  handleReplyClick
}) {
  const user = useSelector(state => state.user);

  const commentText = comment.is_deleted ? "[deleted]" : comment.comment_text;

  const renderUsername = () => {
    if (comment.is_deleted) {
      return "[deleted]";
    }
    return (
      <Link to={"/user/" + comment.author_uuid}>{comment.author_username}</Link>
    );
  };

  return (
    <Wrapper>
      <Body>
        <Header>
          {renderUsername()} on{" "}
          {convertDate(comment.date_submitted) +
            (comment.is_edited
              ? " [Edited on " + convertDate(comment.date_edited) + "]"
              : "")}
        </Header>
        <Text>{commentText}</Text>
      </Body>
      <BottomBar>
        <Icons>
        <Icon
          //onClick={handleThumbsUp}
          hoverColor="#2eaa3a"
          //enabled={post.vote_type === 1}
        >
          <FontAwesomeIcon size="1x" icon={faThumbsUp}></FontAwesomeIcon>
        </Icon>
        <Points points={0}>0</Points>
        <Icon
          //onClick={handleThumbsDown}
          hoverColor="#e2493b"
          //enabled={post.vote_type === -1}
        >
          <FontAwesomeIcon
            size="1x"
            flip="horizontal"
            icon={faThumbsDown}
          ></FontAwesomeIcon>
        </Icon>
      </Icons>
        {!comment.is_deleted && (
          <React.Fragment>
            <RightSide>
              <BottomBarButton onClick={handleReplyClick}>Reply</BottomBarButton>
              {user && user.user_uuid === comment.author_uuid && (
                <BottomBarButton onClick={handleEditClick}>
                  Edit
                </BottomBarButton>
              )}
              {user && ((user.user_uuid === comment.author_uuid) ||
                user.is_admin) && (
                <BottomBarButton onClick={handleDeleteClick}>
                  Delete
                </BottomBarButton>
              )}
            </RightSide>
          </React.Fragment>
        )}
      </BottomBar>
    </Wrapper>
  );
}
