import React from "react";
import styled from "styled-components";

const Display = styled.div`
  background-color: white;
  padding: 25px;
  border-radius: 15px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  color: ${({ theme }) => (theme ? theme.primaryTextColor : "#131516")};
  box-shadow: 5px 7px 0px rgba(0, 0, 0, 0.25);
`;

export default function Comment({ comment }) {
  return (
    <Display>
      <p>{comment.comment_text}</p>
    </Display>
  );
}
