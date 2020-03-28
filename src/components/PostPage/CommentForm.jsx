import React, { useState, useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import FormTextArea from "../styled/FormTextArea";
import FormButton from "../styled/FormButton";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-top: 5px;
`;

const SubmitButton = styled(FormButton)`
  margin: 5px 0px;
  padding: 10px;
`;

export default function CommentForm({ handleSubmit, ...inputProps }) {
  const [comment, setComment] = useState("");
  const theme = useContext(ThemeContext);

  const handleCommentSubmit = e => {
    e.preventDefault();
    handleSubmit(comment);
  }

  return (
    <Wrapper>
      <FormTextArea
        {...inputProps}
        handleInputChange={setComment}
        value={comment}
      />
      <SubmitButton theme={theme} onClick={handleCommentSubmit}>
        Submit
      </SubmitButton>
    </Wrapper>
  );
}
