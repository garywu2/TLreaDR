import React from "react";
import styled from 'styled-components';
import ProfileDisplay from './ProfileDisplay'

const Wrapper = styled.div`
  margin: 10px 0px 30px;
`

const ProfilePage = () => {
    return (
        <Wrapper>
            <ProfileDisplay />
        </Wrapper>
    );
}

export default ProfilePage;