import styled from 'styled-components';

const Label = styled.span`
  padding: 5px 10px;
  border-radius: 3px;
  background-color: ${({ theme }) => (theme ? theme.primaryColor : "#ef3e36")};
  color: ${({ theme }) => (theme ? theme.secondaryTextColor : "#fff")};
  margin: 5px 0px;
  align-self: flex-end;
`

export default Label;