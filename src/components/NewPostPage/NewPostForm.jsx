import React, { useState, useContext } from "react";
import FormInput from "../styled/FormInput";
import FormDropdown from "../styled/FormDropdown";
import styled, { ThemeContext } from "styled-components";
import FormButton from "../styled/FormButton";
import { useSelector } from "react-redux";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheckSquare, faSquare} from "@fortawesome/free-regular-svg-icons";
import { autoSummarizePost } from "../../actions/posts"

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
  const [autoSummarize, setAutoSummarize] = useState(false);
  const [summarizerStatus, setSummarizerStatus] = useState(null);
  const { category, title, body, image_link, article_link } = formValues;
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
  const setArticleLink = article_link => setFormValues(prevState => ({...prevState, article_link}));

  const setArticleInfo = article_link => {
    setArticleLink(article_link);
    
    if(autoSummarize){
      if(isValidUrl(article_link)){
        setSummarizerStatus("Summarizing...");
        autoSummarizePost(article_link).then(data => {
          if(!data.hasOwnProperty('sm_api_error')){
            const summaryBody = data.sm_api_content;
            const summaryTitle = data.sm_api_title;
            setBody(summaryBody);
            setTitle(summaryTitle);
            setSummarizerStatus("Summarized!");
          }else{
            setSummarizerStatus("Error summarizing article");
          }
        });
      }else{
        setSummarizerStatus("Invalid URL");
      }
    }
  }

  function isValidUrl(string) {
    try {
      new URL(string);
    } catch (_) {
      return false;  
    }
  
    return true;
  }

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

const AutoSummarizeMessage = styled.span`
  cursor: pointer;
  color: ${({ theme }) => theme.primaryTextColor};
`;

const Icon = styled.span`
  margin-right: 10px;
`;

  const handleAutoSummarizeClick = () => {
    setAutoSummarize(!autoSummarize);
  };

  return (
    <Wrapper onSubmit={handleFormSubmit}>
        <div>
          <AutoSummarizeMessage theme={theme} onClick={handleAutoSummarizeClick}>
            <Icon>
              <FontAwesomeIcon
                icon={autoSummarize ? faCheckSquare : faSquare}
                size="lg"
              ></FontAwesomeIcon>
            </Icon>
            Auto Summarize Article
          </AutoSummarizeMessage>
      </div>
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
      <FormInput
        label="Article Link (optional)"
        handleInputChange={setArticleInfo}
        value={article_link}
        triedSubmit={invalidSubmit}
      />
      {(summarizerStatus !== null) && (<label>{summarizerStatus}</label>)}
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
