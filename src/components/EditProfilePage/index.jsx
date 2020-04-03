import React, { useState } from "react";
import { useLocation } from "react-router";
import { getProfileFromUserUuid } from "../../actions/users";
import { useHistory } from "react-router-dom";
import EditProfile from "./editProfile";

const EditProfilePage = () => {
  const location = useLocation();
  const history = useHistory();
  const [hasErrors, setHasErrors] = useState(false);
  const user_uuid = location.pathname.split("/user/edit/").reverse()[0];

  const handleEdits = async (new_email, new_username, new_password) => {
    try {
      console.log(user_uuid + new_email + new_username + new_password);
      await getProfileFromUserUuid(user_uuid, new_email, new_username, new_password);
      history.push("/user/" + user_uuid);
    } catch (error) {
      console.log(error);
      setHasErrors(true);
    }
  };
  
  return (
    <div>
      <h1>User Profile</h1>
        <EditProfile handleSubmit={handleEdits} hasErrors={hasErrors}></EditProfile>
    </div>
  );
};


export default EditProfilePage;
