import React, {useState} from "react";
import styled from "styled-components";
import Comment from "./Comment";
import FormInput from "../styled/FormInput"
import CommentInput from "../styled/CommentInput";

const Title = styled.h2`
  color: white;
  margin: 10px 0px;
`;

const postACommentTheme = {
  primaryColor: "#47FFDD",
  darkerColor: "#479ADD",
  primaryTextColor: "#131516",
  secondaryTextColor: "#fff",
}

export default function CommentsList({ comments, handleComment}) {
  console.log(comments);
  const [comment, setComment] = useState("");

  const handleFormSubmit= (e) => {
    e.preventDefault();
    handleComment(comment);
  }

  return (
    <div onSubmit={handleFormSubmit}>
      {comments ? (
        <div>
          <Title>Comments</Title>
          {comments.map(comment => (
            <Comment key={comment.comment_uuid} comment={comment}></Comment>
          ))}
        </div>
      ) : (
        "Loading..."
      )}
      <Title>Post a comment</Title>
      <FormInput 
        handleInputChange={setComment}
        value={comment}
      />
      <CommentInput
        theme={postACommentTheme}>Comment!</CommentInput>
    </div>
    
  );
}
