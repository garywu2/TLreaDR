import React from "react";
import styled from "styled-components";

const ProfilePreview = ({ profile }) => {

  const PreviewBodySupplementary = styled.div`
  display: flex;
  font-size: 15px;
  font-family: "Montserrat", "sans-serif";
`;
 

  return (
  <div>
    <h1>Name</h1>
    <h2>Email</h2>
    <h3>Bio</h3>

  </div>
  );
};

export default ProfilePreview;
