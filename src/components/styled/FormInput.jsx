import styled from "styled-components";
import React from "react";

const Input = styled.input`
  width: 100%;
`

export default props => {
  const { type, hasError, label, handleInputChange, ...inputProps } = props;

  const updateInput = e =>
    handleInputChange && handleInputChange(e.target.value);

  return (
    <div>
      <div style={{ marginLeft: "5px" }}>
        <label className={props}>{label}</label>
      </div>
      <div>
        <Input
          {...inputProps}
          type={type || "text"}
          onChange={updateInput}
          className={props.hasError ? "error" : ""}
        />
      </div>
    </div>
  );
};
