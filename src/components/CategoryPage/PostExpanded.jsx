import React, { useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-regular-svg-icons";
import { faCaretUp } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";

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
  color: ${({ hoverColor, enabled }) => (enabled ? hoverColor : "#828282")};
  cursor: pointer;

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

const Points = styled.div`
  color: ${({ points }) => (points < 0 ? "red" : "black")};
  text-align: center;
  margin: 10px 0px;
  font-weight: bold;
  font-family: Arvo, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
`;

const Title = styled.h2`
  text-decoration: none;
  color: inherit;
`;

const ArticleLink = styled.div`
  margin: 15px 0px 15px 0px;
  color: ${({ theme }) => theme.primaryColor};

  & :hover {
    color: #000000;
  }
`;

export default function PostExpanded({
  post,
  handleThumbsUp,
  handleThumbsDown,
  handleExpand
}) {
  const theme = useContext(ThemeContext);

  const renderArticleButton = () => {
    return (
      <div>
        {post.article_link && (
          <ArticleLink theme={theme}>
            <a target="_blank" href={post.article_link}>
              Article Link
            </a>
          </ArticleLink>
        )}
      </div>
    );
  };

  return (
    <Display theme={theme}>
      <Icons>
        <Icon
          onClick={handleThumbsUp}
          hoverColor="#2eaa3a"
          enabled={post.vote_type === 1}
        >
          <FontAwesomeIcon size="2x" icon={faThumbsUp}></FontAwesomeIcon>
        </Icon>
        <Points points={post.votes}>{post.votes}</Points>
        <Icon
          onClick={handleThumbsDown}
          hoverColor="#e2493b"
          enabled={post.vote_type === -1}
        >
          <FontAwesomeIcon
            size="2x"
            flip="horizontal"
            icon={faThumbsDown}
          ></FontAwesomeIcon>
        </Icon>
      </Icons>
      <Body>
        <Header>
          {post.post_uuid ? (
            <Link to={`/post/${post.post_uuid}`}>
              <Title>{post.title}</Title>
            </Link>
          ) : (
            <Title>{post.title}</Title>
          )}
          <small>
            by{" "}
            <Link to={"/user/" + post.author_uuid}>{post.author_username}</Link>{" "}
            on {convertDate(post.pub_date)}
          </small>
        </Header>
        <Img theme={theme} src={post.image_link}></Img>
        <p>{post.body}</p>
        {renderArticleButton()}
      </Body>
      <Icon onClick={handleExpand}>
        <FontAwesomeIcon size="2x" icon={faCaretUp}></FontAwesomeIcon>
      </Icon>
    </Display>
  );
}
