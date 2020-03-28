import React, { useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-regular-svg-icons";

const Wrapper = styled.div`
  background-color: #e9e9e9;
  border-radius: 8px;
`;

const Body = styled.div`
  padding: 10px;
`;

const Points = styled.div`
  color: ${({ points }) => (points < 0 ? "red" : points === 0 ? "black" : "green")};
  text-align: center;
  margin-right: 10px;
  font-weight: bold;
  font-family: Arvo, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
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
`;

const Icons = styled.div`
  display: flex;
  padding: 0 10px;
  align-items: center;
`;

const Icon = styled.div`
  color: #828282;
  cursor: pointer;

  & :hover {
    color: ${({ hoverColor }) => hoverColor || "#131516"};
  }

  & > svg {
    transition: color 0.1s linear;
  }
`;
const BottomBarButton = styled.button`
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

export default function Comment({ comment, handleReplyClick }) {
  const theme = useContext(ThemeContext);

  const handleThumbsDown = () => {
    console.log("handleThumbsDown called");
  };

  const handleThumbsUp = () => {
    console.log("handleThumbsUp called");
  };

  const commentScore = comment.comment_upvotes - comment.comment_downvotes;

  return (
    <Wrapper>
        <Body>
          <Header>Placeholder on 2020-03-26</Header>
          {/* <Header>
            <Link to={"/user/" + comment.author.username}>
              {comment.author.username}
            </Link>{" "}
            on {comment.pub_date}
          </Header> */}
          <Text>{comment.comment_text}</Text>
        </Body>
        <BottomBar>
          <BottomBarButton onClick={handleReplyClick}>Reply</BottomBarButton>
          <Icons>
            <Points points={commentScore}>
              {commentScore > 0 && "+"}
              {commentScore}
            </Points>
            <Icon onClick={handleThumbsUp} hoverColor="#2eaa3a">
              <FontAwesomeIcon size="lg" icon={faThumbsUp}></FontAwesomeIcon>
            </Icon>
            <Icon onClick={handleThumbsDown} hoverColor="#e2493b">
              <FontAwesomeIcon
                size="lg"
                flip="horizontal"
                icon={faThumbsDown}
              ></FontAwesomeIcon>
            </Icon>
          </Icons>
        </BottomBar>
    </Wrapper>
  );
}
