import React, { useContext } from "react";
import { useLocation } from "react-router-dom";
import styled, { ThemeContext } from "styled-components";

const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-radius: 15px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
`;

const Header = styled.div`
  border-bottom: 7px solid
    ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  padding-bottom: 10px;
  margin-bottom: 10px;
`;

const ProfileDisplay = () => {
  const location = useLocation();
  const theme = useContext(ThemeContext);

  const userName = location.pathname.split("/").reverse()[0];

  return (
    <Display theme={theme}>
      <Header>
        <h2>{userName}</h2>
      </Header>
    </Display>
  );
};

export default ProfileDisplay;
