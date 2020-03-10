import styled from "styled-components";

export default styled.button`
  padding: 15px 20px;
  background-color: ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  color: ${({ theme }) => (theme ? theme.secondaryTextColor : "#fff")};
  margin: 10px 0px;
  transition: background-color 0.1s linear;
  cursor: pointer;
  border: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  border-radius: 3px;

  &:hover {
    background-color: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  }
`;
