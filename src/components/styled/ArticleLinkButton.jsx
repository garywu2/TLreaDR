import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
  justify-content: flex-end;
`;

const ArticleLink = styled.div`
  padding: 15px 20px;
  background-color: ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  color: ${({ theme }) => (theme ? theme.secondaryTextColor : "#fff")};
  margin: 10px 0px;
  transition: background-color 0.1s linear;
  cursor: pointer;
  border: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  border-radius: 3px;
  font-family: "Prompt", -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  font-size: 12pt;

  &:hover {
    background-color: ${({ theme }) => (theme ? theme.darkerColor : "#c21a11")};
  }}
`;

export default ({ post, theme }) => {
  return (
    <div>
      {post.article_link && (
        <Wrapper>
          <ArticleLink theme={theme}>
            <a target="_blank" href={post.article_link}>
              Article Link
            </a>
          </ArticleLink>
        </Wrapper>
      )}
    </div>
  );
};
