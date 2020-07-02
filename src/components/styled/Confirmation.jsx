import styled from "styled-components";
import React, { useState } from "react";

const ConfirmationMessage = styled.div`
    margin-top: 10px;
    font-weight: bold;
`;

const Button = styled.div`
  cursor: pointer;
  color: #FF0000;
  margin-right: 20px;
  font-weight: bold;

  & :hover {
    color: ${({ hovercolor }) => hovercolor || "#000000"};
  }
`;

const Answer = styled.div`
  display: flex;
  justify-content: flex-start;
  margin-top: 15px;
`;

export default function Confirmation({
    handleYesClick,
    handleNoClick
}) {
    return(
        <div>
            <ConfirmationMessage>
                <div>Are you sure?</div>
            </ConfirmationMessage>
            <Answer>
                <Button onClick={handleYesClick}>
                    <div>Yes</div>
                </Button>
                <Button onClick={handleNoClick}>
                    <div>No</div>
                </Button>
            </Answer>
        </div>
    )
}