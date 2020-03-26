import styled from "styled-components";
import React, { useState } from "react";
import Select from "react-select"

const Labels = styled.div`
  margin-left: 5px;
  display: flex;
  justify-content: space-between;
`;

export default props => {
  const {
    label,
    handleInputChange,
    ...inputProps
  } = props;

  const updateInput = category => {
    handleInputChange && handleInputChange(category.value);
  }

  return (
    <div style={{ margin: "10px 0" }}>
      <Labels>
        <label className={props}>{label}</label>
      </Labels>
      <div style={{color: "black"}}>
        <Select
          {...inputProps}
          onChange={updateInput}
        />
      </div>
    </div>
  );
};
