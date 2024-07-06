"use client";

import styled from 'styled-components';

const UploadContainer = styled.div`
    display:flex;
    flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  background-color: white; 
  max-width: 375px; 
  margin: 0 auto; 
  padding: 20px;
  border: 1px solid #ccc; 
  border-radius: 10px;
`;
const OuterContainer = styled.div`
    display:flex;
    flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  background-color: white; 
 
`;
const UploadImage = styled.div`
  width: 100px;
  height: 200px;
  background-image: url('@/pics/concert.jpeg'); 
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
`;
const UploadIcon = styled.div`
  width: 50px;
  height: 50px;
  background-color: black;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
`;

const UploadButtonStyled = styled.button`
  background-color: #b22222; 
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #d03b3b;
  }
`;

const UploadButton = () => {
  const handleUploadClick = () => {
    // Handle the upload logic here
    alert('Upload button clicked');
  };
  const handleAddClick = () => {
    // Handle the upload logic here
    alert('Add button clicked');
  };

  return (
    <UploadContainer>
      <UploadImage>
        <UploadIcon onClick={handleAddClick}>+</UploadIcon>
      </UploadImage>
      <UploadButtonStyled onClick={handleUploadClick}>
        Upload Video
      </UploadButtonStyled>
    </UploadContainer>
    
  );
};

export default UploadButton;
