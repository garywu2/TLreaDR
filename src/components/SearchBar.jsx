import React, { useState } from "react";
import styled from "styled-components";
import { useHistory } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

const FontAwesomeSearchIcon = styled(FontAwesomeIcon)`
  font-size: 2em;
  cursor: pointer;
`;

const SearchBarInputForm = styled.input`
  margin: 10px 20px;
`;

const SearchBarWrapper = styled.div`
  display: flex;
  align-items: center;
`;

const SearchBar = () => {
  const [searchInput, setSearchInput] = useState("");
  const history = useHistory();

  const checkForEnter = e => {
    if (e.key === "Enter") {
      redirectToSearch();
    }
  };

  const redirectToSearch = () => {
    history.push(`/search/${searchInput}`);
    setSearchInput("");
  };

  const handleInputChange = e => {
    setSearchInput(e.target.value);
  };

  return (
    <SearchBarWrapper>
      <FontAwesomeSearchIcon icon={faSearch} onClick={redirectToSearch} />
      <SearchBarInputForm
        type="text"
        onChange={handleInputChange}
        value={searchInput}
        onKeyDown={checkForEnter}
        placeholder="Search..."
      />
    </SearchBarWrapper>
  );
};

export default SearchBar;
