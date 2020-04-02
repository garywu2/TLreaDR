import React, { useState, useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";
import FormInput from "../styled/FormInput";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-top: 5px;
  background-color: #fff;
  padding: 10px 20px;
`;

const CreateButton = styled(FormButton)`
  margin: 5px 0px;
  padding: 10px;
`;

const ErrorMessage = styled.div`
  visibility: ${props => (props.visible ? "visible" : "hidden")};
  text-align: center;
  color: #ff2a2a;
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

export default function CategoryForm({ handleSubmit, hasErrors }) {
  const [categoryName, setCategoryName] = useState("");
  const [invalidSubmit, setInvalidSubmit] = useState("");
  const theme = useContext(ThemeContext);

  const [categoryError] = useErrorCheck(
    [categoryName],
    field => field.length === 0
  );

  const handleCategorySubmit = e => {
    e.preventDefault();
    if (categoryError) {
      setInvalidSubmit(true);
    } else {
      handleSubmit(categoryName);
    }
  };

  return (
    <Wrapper>
      <FormInput
        label="Category Name"
        handleInputChange={setCategoryName}
        value={categoryName}
        hasError={categoryError}
        triedSubmit={invalidSubmit}
        errorMessage="Category name cannot be blank!"
      />
      <CreateButton theme={theme} onClick={handleCategorySubmit}>
        Create
      </CreateButton>
      <ErrorMessage visible={hasErrors}>
        That category already exists.
      </ErrorMessage>
    </Wrapper>
  );
}
