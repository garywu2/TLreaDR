import React from "react";
import logo from "../assets/TLreaDR-logo.png";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

const NavbarWrapper = styled.div`
  width: 100%;
  background-color: #ef3e36;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 25px;
`;

const Button = styled.a`
  float: right;
  color: #ffffff;
  font-size: 18px;
  font-family: "Montserrat", "sans-serif";
  text-decoration: none;
`;

const LogoImage = styled.img`
  width: 11%;
  height: 11%;
`;

const SubheaderWrapper = styled.div`
  list-style-type: none;
  margin: 0;
  padding: 0;
  width: 100%;
  background-color: #d52828;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const CategoryButton = styled.div`
  float: left;
`;

const Anchor = styled.a`
  display: block;
  padding: 14px 16px;
  color: white;
  text-align: center;
  text-decoration: none;
  font-family: "Arvo", sans-serif;
`;

const SearchBar = styled.input`
  float: right;
  margin: 10px 25px;
`;

const Search = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`

const Navbar = () => {
  return (
    <React.Fragment>
      <NavbarWrapper>
        <div></div>
        <LogoImage src={logo} alt="TLreaDR" />
        <Button href="/sign-in">Sign In</Button>
      </NavbarWrapper>
      <SubheaderWrapper>
        <div>
          <CategoryButton>
            <Anchor href="/home">Home</Anchor>
          </CategoryButton>
          <CategoryButton>
            <Anchor href="/News">News</Anchor>
          </CategoryButton>
          <CategoryButton>
            <Anchor href="/Sports">Sports</Anchor>
          </CategoryButton>
          <CategoryButton>
            <Anchor href="/Lifestyle">Lifestyle</Anchor>
          </CategoryButton>
        </div>
        <Search>
          <FontAwesomeIcon size="2x" icon={faSearch} />
          <SearchBar type="text" placeholder="Search..."></SearchBar>
        </Search>
      </SubheaderWrapper>
    </React.Fragment>
  );
};

export default Navbar;
