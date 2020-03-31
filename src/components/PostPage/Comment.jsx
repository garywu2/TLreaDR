import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";
import { useSelector } from "react-redux";

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
      <Link to={"/user/" + comment.author_username}>
        {comment.author_username}
      </Link>
    );
  };

  return (
    <Wrapper>
      <Body>
        <Header>
          {renderUsername()} on {convertDate(comment.date_submitted)}
        </Header>
        <Text>{commentText}</Text>
      </Body>
      <BottomBar>
        {!comment.is_deleted && (
          <React.Fragment>
            <BottomBarButton onClick={handleReplyClick}>Reply</BottomBarButton>
            {user && user.user_uuid === comment.author_uuid && (
              <RightSide>
                <BottomBarButton onClick={handleEditClick}>
                  Edit
                </BottomBarButton>
                <BottomBarButton onClick={handleDeleteClick}>
                  Delete
                </BottomBarButton>
              </RightSide>
            )}
          </React.Fragment>
        )}
      </BottomBar>
    </Wrapper>
  );
}
