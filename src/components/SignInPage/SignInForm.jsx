import React, { useState, useContext } from "react";
import FormInput from "../styled/FormInput";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";
import FormLink from "../styled/FormLink";
import { Link } from "react-router-dom";
import { string } from "prop-types";

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

const WordFormat = styled.div`
  visibility: ${props => props.visible ? "visible" : "hidden"};
  text-align: center;
  color: #FF2A2A;
`;

const signUpTheme = {
  primaryColor: "#03FF14",
  darkerColor: "#52C180",
  primaryTextColor: "#131516",
  secondaryTextColor: "#fff"
}


export default function SignInForm({ handleSubmit, hasErrors }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const theme = useContext(ThemeContext);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSubmit(username, password);
  };

  return (
    <Wrapper onSubmit={handleFormSubmit}>
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
      <WordFormat visible={hasErrors}>
        Account not found, please try again!
        </WordFormat>
      <Row>
        <FormLink to='/sign-up'
          theme={signUpTheme}>Sign Up</FormLink>
        <FormButton theme={theme}>Sign In</FormButton>
      </Row>
    </Wrapper>
  );
}