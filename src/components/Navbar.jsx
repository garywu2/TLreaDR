import React, { useEffect } from "react";
import logo from "../assets/TLreaDR-logo.png";
import styled from "styled-components";
import { Link, useHistory } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { LOGOUT_USER } from "../actions/types";
import { getCategories } from "../actions/categories";
import SearchBar from "./SearchBar";

const NavbarWrapper = styled.div`
  background-color: #ef3e36;
  display: flex;
  align-items: center;
  padding: 10px 25px;
`;

const NavbarHeaderChild = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;

  &:last-child > div {
    margin-left: auto;
  }
`;

const LoggedInButton = styled.a`
  color: #ffffff;
  font-size: 15px;
  font-family: "Montserrat", "sans-serif";
  text-decoration: none;
  cursor: pointer;
  padding: 15px 10px;
  margin: 3px;
`;

const LoggedOutButton = styled(Link)`
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
        console.log(e);
      }
    };

    getAllCategories();
  }, [getCategories]);

  const renderCategories = () => {
    if (!categories) {
      return <div></div>;
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

  const renderMenuButtons = () => {
    return (
      <NavbarHeaderChild>
        {userAccount ? (
          <div>
            <LoggedInButton onClick={viewProfileButtonClick}>Profile</LoggedInButton>
            <LoggedInButton onClick={newPostButtonClick}>New Post</LoggedInButton>
            <LoggedInButton onClick={handleLogout}>Log Out</LoggedInButton>
          </div>
        ) : (
          <div>
            <LoggedOutButton to="/sign-in">Sign In</LoggedOutButton>
          </div>
        )}
      </NavbarHeaderChild>
    );
  };

  const viewProfileButtonClick = () => {
    history.push(`/user/${userAccount.username}`);
  };

  const newPostButtonClick = () => {
    history.push('/new');
  }

  const handleLogout = () => {
    dispatch({ type: LOGOUT_USER });
    history.push("/");
  };

  return (
    <React.Fragment>
      <NavbarWrapper>
        <NavbarHeaderChild></NavbarHeaderChild>
        <NavbarHeaderChild>
          <LogoImage src={logo} alt="TLreaDR" />
        </NavbarHeaderChild>
        {renderMenuButtons()}
      </NavbarWrapper>
      <SubheaderWrapper>
        {renderCategories()}
        <SearchBar />
      </SubheaderWrapper>
    </React.Fragment>
  );
};

export default Navbar;
