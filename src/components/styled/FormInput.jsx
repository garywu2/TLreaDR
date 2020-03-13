import styled from "styled-components";
import React, { useState } from "react";

const Labels = styled.div`
  margin-left: 5px;
  display: flex;
  justify-content: space-between;
`;

const ErrorMessage = styled.label`
  color: red;
  visibility: ${({ showError }) => (showError ? "visible" : "hidden")};
`;

const Input = styled.input`
  width: 100%;
`;

export default props => {
  const {
    type,
    hasError,
    errorMessage,
    label,
    handleInputChange,
    triedSubmit,
    ...inputProps
  } = props;
  const [touched, setTouched] = useState(false);

  const updateInput = e =>
    handleInputChange && handleInputChange(e.target.value);

  const showError = hasError && (touched || triedSubmit);

  return (
    <div style={{ margin: "10px 0" }}>
      <Labels>
        <label className={props}>{label}</label>
        <ErrorMessage showError={showError}>{errorMessage}</ErrorMessage>
      </Labels>
      <div>
        <Input
          {...inputProps}
          type={type || "text"}
          onBlur={() => setTouched(true)}
          onChange={updateInput}
          className={showError ? "error" : ""}
        />
      </div>
    </div>
  );
};
