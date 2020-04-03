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
    margin: 0px 10px;
  }
`;

const WordFormat = styled.div`
  visibility: ${props => props.visible ? "visible" : "hidden"};
  text-align: center;
  color: #FF2A2A;
`;

const profileTheme = {
  primaryColor: "#03FF14",
  darkerColor: "#52C180",
  primaryTextColor: "#131516",
  secondaryTextColor: "#fff"
}


export default function editProfile({handleSubmit}) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const theme = useContext(ThemeContext);
  const user_uuid = location.pathname.split("/user/edit/").reverse()[0];

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSubmit(email, username, password);
  };

  return (
    <Wrapper onSubmit={handleFormSubmit}>
      <FormInput
        label="Email"
        handleInputChange={setEmail}
        value={email}
        autocomplete="email"
      />
      <FormInput
        label="username"
        handleInputChange={setUsername}
        value={username}
        autocomplete="username"
      />
      <FormInput
        label="Password"
        handleInputChange={setPassword}
        value={password}
        autocomplete= "password"
      />
      <Row>
        <FormButton theme={theme}>Finish Edits</FormButton>
      </Row>
    </Wrapper>
  );
}