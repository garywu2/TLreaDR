import React, { useState } from "react";
import FormInput from "../styled/FormInput";
import styled from "styled-components";

const Wrapper = styled.div`
  background-color: white;  
  padding: 10px 20px;
`

const Row = styled.div`
  display: flex;
  margin: 15px 0px;

  & > * {
    flex: 1;
  }
`;

export default function SignupForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <Wrapper>
      <Row>
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
      </Row>
      <FormInput
        hasError={false}
        label="Email address"
        handleInputChange={setUsername}
        value={username}
        autocomplete="email"
      />
    </Wrapper>
  );
}
