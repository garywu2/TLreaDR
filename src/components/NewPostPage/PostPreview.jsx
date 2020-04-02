import React, { useState } from "react";
import { useSelector } from "react-redux";
import PostExpanded from "../CategoryPage/PostExpanded";
import styled from "styled-components";

const Header = styled.h2`
  color: white;
  margin: 10px 0px;
`;

export default function PostPreview({ formValues }) {
  const [fakeVotes, setFakeVotes] = useState(0);
  const [fakeDownvotes, setFakeDownvotes] = useState(0);

  const userAccount = useSelector(state => state.user);

  const handleThumbsUp = () => setFakeVotes(fakeVotes + 1);
  const handleThumbsDown = () => setFakeVotes(fakeDownvotes - 1);

  const title = formValues.title.length ? formValues.title : "Your title here";
  const body = formValues.body.length ? formValues.body : "Your TL;DR here";

  const date = new Date().toLocaleDateString();

  const placeholderImage =
    "https://www.peakfitness.co.nz/wp-content/uploads/2016/02/placeholder-10.jpg";

  const image_link = formValues.image_link.length
    ? formValues.image_link
    : placeholderImage;

  const post = {
    title,
    body,
    pub_date: date,
    votes: fakeVotes,
    image_link,
    author: userAccount
  };

  return userAccount ? (
    <div>
      <Header>Post Preview</Header>
      <PostExpanded
        post={post}
        handleThumbsUp={handleThumbsUp}
        handleThumbsDown={handleThumbsDown}
      ></PostExpanded>
    </div>
  ) : (
    <div>Loading...</div>
  );
}
