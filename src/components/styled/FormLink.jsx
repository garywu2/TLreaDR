import styled from "styled-components";
import {Link} from "react-router-dom";
export default styled(Link)`
  padding: 15px 20px;
  background-color: ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  color: ${({ theme }) => (theme ? theme.secondaryTextColor : "#fff")};
  margin: 10px 0px;
  transition: background-color 0.1s linear;
  cursor: pointer;
  border: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  border-radius: 3px;
  text-align: center;
  text-decoration: none;
  font-family: "Prompt", -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 12pt;

  &:hover {
    background-color: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  }
`;
