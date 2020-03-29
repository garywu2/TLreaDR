import React, { useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretDown } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";

const Display = styled.div`
  background-color: white;
  padding: 15px 25px;
  border-radius: 15px;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
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
  object-fit: cover;
  width: 250px;
  max-height: 144px;
`;

const Title = styled.h2`
  cursor: pointer;
  text-decoration: none;
  color: inherit;
`;

export default function PostPreview({ post, handleExpand }) {
  const theme = useContext(ThemeContext);

  return (
    <Display>
      <Img theme={theme} src={post.image_link}></Img>
      <Body>
        <Header>
          <Link to={`/post/${post.post_uuid}`}>
            <Title>{post.title}</Title>
          </Link>
          <small>
            by{" "}
            <Link to={"/user/" + post.author.user_uuid}>
              {post.author.username}
            </Link>{" "}
            on {convertDate(post.pub_date)}
          </small>
        </Header>
      </Body>
      <Icon>
        <FontAwesomeIcon
          onClick={handleExpand}
          size="2x"
          icon={faCaretDown}
        ></FontAwesomeIcon>
      </Icon>
    </Display>
  );
}
