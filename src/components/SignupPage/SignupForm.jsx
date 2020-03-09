import React, { useState, useContext } from "react";
import FormInput from "../styled/FormInput";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";

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
  }
`;

export default function SignupForm({handleSubmit}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const theme = useContext(ThemeContext);

  return (
    <Wrapper onSubmit={handleSubmit}>
      <FormInput
        hasError={false}
        label="Username"
        handleInputChange={setUsername}
        value={username}
        autocomplete="username"
      />
      <FormInput
        hasError={false}
        label="Password"
        handleInputChange={setPassword}
        value={password}
        type="password"
        autocomplete="new-password"
      />

      <FormInput
        hasError={false}
        label="Email address"
        handleInputChange={setUsername}
        value={username}
        autocomplete="email"
      />
      <FormButton theme={theme}>Sign Up</FormButton>
    </Wrapper>
  );
}
