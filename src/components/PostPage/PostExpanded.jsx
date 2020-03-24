import React, { useContext, useState } from "react";
import styled, { ThemeContext } from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-regular-svg-icons";
import { faCaretUp } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

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

export default function PostExpanded({ post, handleExpand }) {
  const [expanded, setExpanded] = useState(false);
  const theme = useContext(ThemeContext);

  const handleThumbsUp = () => {
    console.log("handleThumbsUp called");
  };

  const handleThumbsDown = () => {
    console.log("handleThumbsDown called");
  };

  return (
    <Display theme={theme}>
      <Icons>
        <Icon onClick={handleThumbsUp} hoverColor="#2eaa3a">
          <FontAwesomeIcon size="2x" icon={faThumbsUp}></FontAwesomeIcon>
        </Icon>
        <Icon onClick={handleThumbsDown} hoverColor="#e2493b">
          <FontAwesomeIcon
            size="2x"
            flip="horizontal"
            icon={faThumbsDown}
          ></FontAwesomeIcon>
        </Icon>
      </Icons>
      <Body>
        <Header>
          <h2>{post.title}</h2>
          <small>
            by{" "}
            <Link to={"/user/" + post.author.username}>
              {post.author.username}
            </Link>{" "}
            on {post.pub_date.slice(0, 10).replace(/-/g, "/")}
          </small>
        </Header>
        <Img theme={theme} src={post.image_link}></Img>
        <p>{post.body}</p>
      </Body>
      <Icon onClick={handleExpand}>
        <FontAwesomeIcon size="2x" icon={faCaretUp}></FontAwesomeIcon>
      </Icon>
    </Display>
  );
}
