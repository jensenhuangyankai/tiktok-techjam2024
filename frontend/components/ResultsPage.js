import React from 'react';
import styled from 'styled-components';

const ResultsPage = ({ videoTags, audioTags }) => {
  const renderTags = (tags) => {
    return Object.keys(tags).map((tag) => (
      <Tag key={tag}>
        {tag}
      </Tag>
    ));
  };

  return (
    <ResultsContainer>
      <HeaderText>Processed Video</HeaderText>
      <TagsContainer>
        <TagSection>
          <SectionHeader>Video Tags</SectionHeader>
          <TagList>
            {renderTags(videoTags)}
          </TagList>
        </TagSection>
        <TagSection>
          <SectionHeader>Audio Tags</SectionHeader>
          <TagList>
            {renderTags(audioTags)}
          </TagList>
        </TagSection>
      </TagsContainer>
    </ResultsContainer>
  );
};

const ResultsContainer = styled.div`
  padding: 20px;
  text-align: center;
`;

const HeaderText = styled.h1`
  color: black; /* Set font color to black */
  font-size: 2.5rem;
  margin-bottom: 20px;
`;

const TagsContainer = styled.div`
  margin-top: 20px;
`;

const TagSection = styled.div`
  margin-bottom: 20px;
`;

const SectionHeader = styled.h2`
  color: black; /* Set font color to black */
  font-size: 1.8rem;
  margin-bottom: 10px;
`;

const TagList = styled.ul`
  list-style: none;
  padding: 0;
`;

const Tag = styled.li`
  display: inline-block;
  background: #f0f0f0;
  color: black; /* Set font color to black */
  margin: 5px;
  padding: 10px;
  border-radius: 5px;
`;

export default ResultsPage;
