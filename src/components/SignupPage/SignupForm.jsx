import React, { useState, useContext } from "react";
import FormInput from "../styled/FormInput";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSquare, faCheckSquare } from "@fortawesome/free-regular-svg-icons";

const Wrapper = styled.form`
  background-color: white;
  padding: 10px 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
`;

const ErrorMessage = styled.div`
  visibility: ${props => (props.visible ? "visible" : "hidden")};
  text-align: center;
  color: #ff2a2a;
`;

const Icon = styled.span`
  margin-right: 10px;
`;

const AdminMessage = styled.span`
  cursor: pointer;
  color: ${({ theme }) => theme.primaryTextColor};
`;

/**
 * Check for all errors in the redux forms
 * @param {Array[String]} fields The values of form fields
 * @param {Function} errCondition A callback function that is true is the field has an error
 */
const useErrorCheck = (fields, errCondition) => {
  const errors = [];

  // true if empty
  fields.forEach(field => errors.push(errCondition(field)));
  // return errors in the same order

  return errors;
};

export default function SignupForm({ handleSubmit, hasErrors }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [validEmail, setValidEmail] = useState(false);
  const [adminKey, setAdminKey] = useState("");
  const [invalidSubmit, setInvalidSubmit] = useState(false);
  const theme = useContext(ThemeContext);
  const [showAdminField, setShowAdminField] = useState(false);

  const [usernameError, passwordError] = useErrorCheck(
    [username, password],
    field => field.length === 0
  );

  const emailError = email.length === 0 || !validEmail

  const adminError = showAdminField && adminKey !== "plsmakemeadmin";

  const handleFormSubmit = e => {
    e.preventDefault();
    if ([usernameError, passwordError, emailError, adminError].includes(true)) {
      setInvalidSubmit(true);
    } else {
      // if showing admin field and passes error, then user is admin
      let isAdmin = showAdminField;

      handleSubmit(email, username, password, isAdmin);
    }
  };

  const handleAdminClick = () => {
    setShowAdminField(!showAdminField);
  };

  const handleValidateEmail = (email) => {
      let validator = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

      setEmail(email);
    if (validator.test(email) ) {
        setValidEmail(true);
    }
    else {
        setValidEmail(false);
    }
  }

  return (
    <Wrapper onSubmit={handleFormSubmit}>
      <FormInput
        label="Username"
        handleInputChange={setUsername}
        value={username}
        autocomplete="username"
        hasError={usernameError}
        triedSubmit={invalidSubmit}
        errorMessage="Username cannot be blank!"
      />
      <FormInput
        label="Password"
        handleInputChange={setPassword}
        value={password}
        type="password"
        autocomplete="current-password"
        hasError={passwordError}
        triedSubmit={invalidSubmit}
        errorMessage="Password cannot be blank!"
      />
      <FormInput
        label="Email address"
        handleInputChange={handleValidateEmail}
        value={email}
        autocomplete="email"
        hasError={emailError}
        triedSubmit={invalidSubmit}
        errorMessage="Invalid Email Address!"
      />
      <div>
          <AdminMessage theme={theme} onClick={handleAdminClick}>
            <Icon>
              <FontAwesomeIcon
                icon={showAdminField ? faCheckSquare : faSquare}
                size="lg"
              ></FontAwesomeIcon>
            </Icon>
            Sign up for an admin account
          </AdminMessage>
      </div>
      {showAdminField && (
        <FormInput
          label="Admin key"
          handleInputChange={setAdminKey}
          value={adminKey}
          hasError={adminError}
          triedSubmit={invalidSubmit}
          errorMessage={"Invalid admin key."}
        />
      )}
      <ErrorMessage visible={hasErrors}>
        That username already exists!
      </ErrorMessage>
      <FormButton theme={theme}>Sign Up</FormButton>
    </Wrapper>
  );
}
