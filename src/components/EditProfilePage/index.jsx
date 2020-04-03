import React, { useEffect, useState, useContext } from "react";
import styled, { ThemeContext } from "styled-components";
import { useLocation } from "react-router";
import { getUserFromUserUuid } from "../../actions/users";
import { getProfileFromUserUuid } from "../../actions/users";
//import { FormButton } from "../styled/FormButton";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import EditProfile from "./editProfile";




const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-radius: 15px;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
`;

const Header = styled.div`
  border-bottom: 7px solid
    ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  padding-bottom: 10px;
  margin-bottom: 10px;
`;

const ButtonWrapper = styled.div`
  display: flex;
  justify-content: flex-start;
`;

const EditProfilePage = () => {
  const [new_username, setnew_username] = useState(null);
  const [new_Email, setnew_Email] = useState(null);
  const [new_password, setnew_Password] = useState(null);
  const theme = useContext(ThemeContext);
  const location = useLocation();
  const [user, setUser] = useState(null);
  const history = useHistory();
  const dispatch = useDispatch();
  const user_uuid = location.pathname.split("/user/edit/").reverse()[0];

  useEffect(() => {
    const getUsername = async () => {
      try {
        const { user } = await getUserFromUserUuid(user_uuid);
        setUser(user);
      } catch (e) {
        console.log(e);
      }
    };
    getUsername();
  }, [
    getProfileFromUserUuid,
    getUserFromUserUuid,
    user_uuid
  ]);

  const handleEdits = async (new_email, new_username, new_password) => {
    try {
      console.log(user_uuid + new_email + new_username + new_password);
      await getProfileFromUserUuid(user_uuid, new_email, new_username, new_password);
      history.push("/user/" + user_uuid);
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div>
      <h1>User Profile</h1>
        <EditProfile handleSubmit={handleEdits}></EditProfile>
    </div>
  );
};


export default EditProfilePage;
