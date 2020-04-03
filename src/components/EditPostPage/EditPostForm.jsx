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

export default function EditPostForm({
  formValues,
  setFormValues,
  handleSubmit,
  hasErrors
}) {
  const theme = useContext(ThemeContext);
  const [invalidSubmit, setInvalidSubmit] = useState(false);
  const { title, body, image_link } = formValues;

  const setTitle = title =>
    setFormValues(prevState => ({ ...prevState, title }));
  const setBody = body => setFormValues(prevState => ({ ...prevState, body }));
  const setImageLink = image_link =>
    setFormValues(prevState => ({ ...prevState, image_link }));

  const [titleError, bodyError] = useErrorCheck(
    [title, body],
    field => field.length === 0
  );

  const handleFormSubmit = e => {
    e.preventDefault();
    if ([titleError, bodyError].includes(true)) {
      setInvalidSubmit(true);
    } else {
      handleSubmit();
    }
  };

  return (
    <Wrapper onSubmit={handleFormSubmit}>
      <FormInput
        label="Post Title"
        handleInputChange={setTitle}
        value={title}
        hasError={titleError}
        triedSubmit={invalidSubmit}
        errorMessage="Title cannot be blank!"
      />
      <FormInput
        label="TL;DR"
        handleInputChange={setBody}
        value={body}
        hasError={bodyError}
        triedSubmit={invalidSubmit}
        errorMessage="TL;DR cannot be blank!"
      />
      <FormInput
        label="Image Link (optional)"
        handleInputChange={setImageLink}
        value={image_link}
        triedSubmit={invalidSubmit}
      />
      <ErrorMessage visible={hasErrors}>
        There was an error on the backend.
      </ErrorMessage>
      <FormButton theme={theme}>Edit Post</FormButton>
    </Wrapper>
  );
}
