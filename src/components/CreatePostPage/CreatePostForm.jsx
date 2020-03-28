import React, { useState, useContext } from "react";
import PostInput from "../styled/PostInput";
import styled, { ThemeContext } from "styled-components";

const Wrapper = styled.form`
  background-color: white;
  padding: 10px 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
`;

const Row = styled.div`
  display: flex;
  margin: 15px 0px;

  & > * {
    flex: 1;
    margin: 0px 10px;
  }
`;


export default function SignInForm({ handleSubmit, hasErrors }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSubmit(username, password);
  };

  return (
    <Wrapper onSubmit={handleFormSubmit}>
      <PostInput
        hasError={false}
        label="Title"
        handleInputChange={setUsername}
        value={username}
        autocomplete="username"
      />
      <PostInput
        hasError={false}
        label="Description"
        handleInputChange={setPassword}
        value={password}
        type="password"
        autocomplete="new-password"
      />
    </Wrapper>
  );
}