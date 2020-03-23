import React, { useState, useContext } from "react";
import FormInput from "../styled/FormInput";
import FormDropdown from "../styled/FormDropdown";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";
import { useSelector } from "react-redux";

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

export default function NewPostForm({
  formValues,
  setFormValues,
  handleSubmit,
  hasErrors
}) {
  const theme = useContext(ThemeContext);
  const [invalidSubmit, setInvalidSubmit] = useState(false);
  const { category, title, body, image_link } = formValues;
  const categories = useSelector(state => state.categories);
  const categoryOptions = categories
    ? categories.map(category => ({
        value: category.name,
        label: category.name[0].toUpperCase() + category.name.slice(1)
      }))
    : [];

  const setCategory = category =>
    setFormValues(prevState => ({ ...prevState, category }));
  const setTitle = title =>
    setFormValues(prevState => ({ ...prevState, title }));
  const setBody = body => setFormValues(prevState => ({ ...prevState, body }));
  const setImageLink = image_link =>
    setFormValues(prevState => ({ ...prevState, image_link }));

  const [categoryError, titleError, bodyError] = useErrorCheck(
    [category, title, body],
    field => field.length === 0
  );

  const handleFormSubmit = e => {
    e.preventDefault();
    if ([categoryError, titleError, bodyError].includes(true)) {
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
      <FormDropdown
        label="Category"
        handleInputChange={setCategory}
        options={categoryOptions}
      />
      <ErrorMessage visible={hasErrors}>
        There was an error on the backend.
      </ErrorMessage>
      <FormButton theme={theme}>Create new post</FormButton>
    </Wrapper>
  );
}
