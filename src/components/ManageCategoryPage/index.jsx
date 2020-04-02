import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { addCategory, deleteCategory } from "../../actions/categories";
import Category from "./Category";
import CategoryForm from "./CategoryForm";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlusCircle, faMinusCircle } from "@fortawesome/free-solid-svg-icons";
import styled from "styled-components";

const Icon = styled(FontAwesomeIcon)`
  color: #fff;
  cursor: pointer;
`;

const Wrapper = styled.div`
  margin-top: 10px;
`

export default function ManageCategoryPage() {
  const user = useSelector(state => state.user);
  const userLoaded = useSelector(state => state.loaded.userLoaded);
  const categories = useSelector(state => state.categories);
  const history = useHistory();
  const dispatch = useDispatch();
  const [showCategoryForm, setShowCategoryForm] = useState(false);
  const [hasErrors, setHasErrors] = useState(false);

  useEffect(() => {
    if (userLoaded && !user) {
      history.push("/category/all");
    }
  }, [user, userLoaded]);

  const handleCategoryAdd = async categoryName => {
    try {
      dispatch(await addCategory(categoryName));
    } catch(e) {
      console.log(e);
      setHasErrors(true);
    }

    setHasErrors(false);
    setShowCategoryForm(false);
  };

  const handleCategoryDelete = async categoryName => {
    try {
      dispatch(await deleteCategory(categoryName));
    } catch(e) {
      console.log(e);
    }
  };

  const renderCategories = () => {
    if (categories) {
      return categories.map(category => (
        <Category
          key={category.category_uuid}
          category={category}
          handleCategoryAdd={handleCategoryAdd}
          handleCategoryDelete={handleCategoryDelete}
        ></Category>
      ));
    }
  };

  const renderNewCategory = () => {
    if (showCategoryForm) {
      return (
        <div>
          <Icon
            size="2x"
            icon={faMinusCircle}
            onClick={() => setShowCategoryForm(false)}
          ></Icon>
          <CategoryForm
            hasErrors={hasErrors}
            handleSubmit={handleCategoryAdd}
          ></CategoryForm>
        </div>
      );
    } else {
      return (
        <div>
          <Icon
            size="2x"
            icon={faPlusCircle}
            onClick={() => setShowCategoryForm(true)}
          ></Icon>
        </div>
      );
    }
  };

  return (
    <Wrapper>
      <h3>Manage Categories</h3>
      {renderCategories()}
      {renderNewCategory()}
    </Wrapper>
  );
}
