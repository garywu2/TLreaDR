import React, { useEffect } from "react";
import logo from "../assets/TLreaDR-logo.png";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { Link, useHistory } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { LOGOUT_USER } from "../actions/types";
import { getCategories } from "../actions/categories";

const NavbarWrapper = styled.div`
  background-color: #ef3e36;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 25px;
`;

const SignOutButton = styled.a`
  color: #ffffff;
  font-size: 18px;
  font-family: "Montserrat", "sans-serif";
  text-decoration: none;
  cursor: pointer;
  padding: 15px 10px;
`;

const SignInButton = styled(Link)`
  color: #ffffff;
  font-size: 18px;
  font-family: "Montserrat", "sans-serif";
  text-decoration: none;
  cursor: pointer;
  padding: 15px 10px;
`;

const LogoImage = styled.img`
  height: 50px;
`;

const SubheaderWrapper = styled.div`
  background-color: #d52828;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const CategoryWrapper = styled.div`
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
`;

const PageReference = styled(Link)`
  padding: 14px 16px;
  color: white;
  text-align: center;
  text-decoration: none;
  font-family: "Arvo", sans-serif;
`;

const SearchBar = styled.input`
  margin: 10px 20px;
`;

const Search = styled.div`
  display: flex;
  align-items: center;
`;

const Navbar = () => {
  const userAccount = useSelector(state => state.user);
  const categories = useSelector(state => state.categories);
  const dispatch = useDispatch();
  const history = useHistory();

  useEffect(() => {
    const getAllCategories = async () => {
      try {
        dispatch(await getCategories());
      } catch (e) {
        error = e;
      }
    };

    getAllCategories();
  }, [getCategories]);

  const renderCategories = () => {
    if (!categories) {
      return null;
    }
    return (
      <CategoryWrapper>
        <div key="all">
          <PageReference to="/category/all">Home</PageReference>
        </div>
        {categories.map(category => (
          <div key={category.name}>
            <PageReference to={"/category/".concat(category.name)}>
              {category.name
                .charAt(0)
                .toUpperCase()
                .concat(category.name.slice(1))}
            </PageReference>
          </div>
        ))}
      </CategoryWrapper>
    );
  };

  const handleLogout = () => {
    dispatch({ type: LOGOUT_USER });
    history.push("/");
  };

  return (
    <React.Fragment>
      <NavbarWrapper>
        <div></div>
        <LogoImage src={logo} alt="TLreaDR" />
        {!userAccount ? (
          <SignInButton to="/sign-in">Sign In</SignInButton>
        ) : (
          <SignOutButton onClick={handleLogout}>Log Out</SignOutButton>
        )}
      </NavbarWrapper>
      <SubheaderWrapper>
        {renderCategories()}
        <Search>
          <FontAwesomeIcon size="2x" icon={faSearch} />
          <SearchBar type="text" placeholder="Search..." />
        </Search>
      </SubheaderWrapper>
    </React.Fragment>
  );
};

export default Navbar;
