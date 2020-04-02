import React from "react";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashAlt, faPlusCircle } from "@fortawesome/free-solid-svg-icons";

const Wrapper = styled.div`
  background-color: #fff;
  display: flex;
  padding: 20px;
  border-radius: 3px;
  color: #131516;
  justify-content: space-between;
  margin: 10px 0px;
`;

const Icon = styled(FontAwesomeIcon)`
  color: gray;
  cursor: pointer;

  & :hover {
    color: #131516;
  }
`;

export default function Category({ category, handleCategoryDelete }) {
  return (
    <Wrapper>
      <div>
        {category.name
          .charAt(0)
          .toUpperCase()
          .concat(category.name.slice(1))}
      </div>
      <Icon
        size="lg"
        icon={faTrashAlt}
        onClick={() => handleCategoryDelete(category.name)}
      ></Icon>
    </Wrapper>
  );
}
