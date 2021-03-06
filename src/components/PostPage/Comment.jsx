import React, {useState} from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import convertDate from "../../utils/convertDate";
import { useSelector } from "react-redux";
import Confirmation from "../styled/Confirmation";

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

const ConfirmationMessage = styled.div`
  display: flex;
  justify-content: flex-end;
  padding: 5px;
`;

export default function Comment({
  comment,
  handleEditClick,
  handleDelete,
  handleReplyClick
}) {
  const user = useSelector(state => state.user);
  const [commentDeleteClicked, setCommentDeleteClicked] = useState(false);

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
        {!comment.is_deleted && (
          <React.Fragment>
            <BottomBarButton onClick={handleReplyClick}>Reply</BottomBarButton>
            <RightSide>
              {user && user.user_uuid === comment.author_uuid && (
                <BottomBarButton onClick={handleEditClick}>
                  Edit
                </BottomBarButton>
              )}
              {user && ((user.user_uuid === comment.author_uuid) ||
                user.is_admin) && (
                <BottomBarButton onClick={() => setCommentDeleteClicked(true)}>
                  Delete
                </BottomBarButton>
              )}
            </RightSide>
          </React.Fragment>
        )}
      </BottomBar>
      <ConfirmationMessage>
        {commentDeleteClicked && (<Confirmation
              handleYesClick={handleDelete}
              handleNoClick={() => setCommentDeleteClicked(false)}>
            </Confirmation>)}
      </ConfirmationMessage>
    </Wrapper>
  );
}
