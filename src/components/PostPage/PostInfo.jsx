import React, { useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-regular-svg-icons";
import { Link, useHistory } from "react-router-dom";
import convertDate from "../../utils/convertDate";
import { upvotePost, downvotePost } from "../../actions/posts";
import { useSelector } from "react-redux";
import ArticleLinkButton from "../styled/ArticleLinkButton";
import Label from "../styled/Label";

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

const Points = styled.div`
  color: ${({ points }) => (points < 0 ? "red" : "black")};
  text-align: center;
  margin: 10px 0px;
  font-weight: bold;
  font-family: Arvo, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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

const Footer = styled.div`
  display: flex;
  justify-content: flex-start;
  margin-top: 15px;
`;

const EditButton = styled(Link)`
  cursor: pointer;
  color: #828282;
  margin-right: 20px;

  & :hover {
    color: ${({ hovercolor }) => hovercolor || "#000000"};
  }
`;

const DeleteButton = styled.div`
  cursor: pointer;
  color: #828282;
  margin-right: 20px;

  & :hover {
    color: ${({ hovercolor }) => hovercolor || "#000000"};
  }
`;

const ErrorMessage = styled.div`
  visibility: ${props => (props.visible ? "visible" : "hidden")};
  text-align: center;
  color: #ff2a2a;
`;

export default function PostInfo({
  post,
  votePost,
  handleDeleteClick,
  hasErrors
}) {
  const theme = useContext(ThemeContext);
  const history = useHistory();
  const user = useSelector(state => state.user);

  const handleThumbsUp = async () => {
    if (user) {
      votePost(
        await upvotePost(post.post_uuid, user.user_uuid, post.vote_type)
      );
    } else {
      history.push("/sign-in");
    }
  };

  const handleThumbsDown = async () => {
    if (user) {
      votePost(
        await downvotePost(post.post_uuid, user.user_uuid, post.vote_type)
      );
    } else {
      history.push("/sign-in");
    }
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
          <div>
            <h2>{post.title}</h2>
            <small>
              by{" "}
              <Link to={"/user/" + post.author_uuid}>
                {post.author_username}
              </Link>{" "}
              on{" "}
              {convertDate(post.pub_date) +
                (post.edited_flag
                  ? " [Edited on " + convertDate(post.edited_date) + "]"
                  : "")}
            </small>
          </div>
          <div>{post.new_flag && <Label>New</Label>}</div>
        </Header>
        <Img theme={theme} src={post.image_link}></Img>
        <p>{post.body}</p>
        <ArticleLinkButton post={post} theme={theme} />
        {user && user.user_uuid === post.author_uuid && (
          <Footer>
            <EditButton
              hovercolor="#62b0d1"
              to={post.post_uuid.concat("/edit")}
            >
              <div>Edit</div>
            </EditButton>
            <DeleteButton hovercolor="#e2493b" onClick={handleDeleteClick}>
              <div>Delete</div>
            </DeleteButton>
          </Footer>
        )}
        <ErrorMessage visible={hasErrors}>
          There was an error on the backend.
        </ErrorMessage>
      </Body>
    </Display>
  );
}
