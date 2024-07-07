import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import styled from 'styled-components';

const ResultsPage = () => {
  const router = useRouter();
  const { videoTags, audioTags } = router.query;
  const [parsedVideoTags, setParsedVideoTags] = useState([]);
  const [parsedAudioTags, setParsedAudioTags] = useState([]);
  const [relatedTags, setRelatedTags] = useState(null);

  useEffect(() => {
    if (videoTags) {
      setParsedVideoTags(JSON.parse(videoTags));
    }
    if (audioTags) {
      setParsedAudioTags(JSON.parse(audioTags));
    }
  }, [videoTags, audioTags]);

  const renderTags = (tags) => {
    return tags.map((tag) => (
      <Tag key={tag}>
        {tag}
      </Tag>
    ));
  };

  const handleGenerateRelatedTags = async () => {
    const fetchRelatedTags = () => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            relatedVideoTags: ["relatedVideoTag1", "relatedVideoTag2"],
            relatedAudioTags: ["relatedAudioTag1", "relatedAudioTag2"]
          });
        }, 1000);
      });
    };

    const relatedTags = await fetchRelatedTags();
    setRelatedTags(relatedTags);
  };

  return (
    <ResultsContainer>
      <HeaderText>Processed Video</HeaderText>
      <TagsContainer>
        <TagSection>
          <SectionHeader>Video Tags</SectionHeader>
          <TagList>
            {renderTags(parsedVideoTags)}
          </TagList>
        </TagSection>
        <TagSection>
          <SectionHeader>Audio Tags</SectionHeader>
          <TagList>
            {renderTags(parsedAudioTags)}
          </TagList>
        </TagSection>
      </TagsContainer>
      <GenerateButton onClick={handleGenerateRelatedTags}>
        Generate Related Hashtags
      </GenerateButton>
      {relatedTags && (
        <RelatedTagsContainer>
          <TagSection>
            <SectionHeader>Related Video Tags</SectionHeader>
            <TagList>
              {renderTags(relatedTags.relatedVideoTags)}
            </TagList>
          </TagSection>
          <TagSection>
            <SectionHeader>Related Audio Tags</SectionHeader>
            <TagList>
              {renderTags(relatedTags.relatedAudioTags)}
            </TagList>
          </TagSection>
        </RelatedTagsContainer>
      )}
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

const GenerateButton = styled.button`
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;

  &:hover {
    background-color: #0056b3;
  }
`;

const RelatedTagsContainer = styled.div`
  margin-top: 40px;
`;

export default ResultsPage;
