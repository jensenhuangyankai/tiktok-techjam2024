"use client";

import Header from '../components/Header';
import MainContent from '../components/MainContent';
import Footer from '../components/Footer';
import styled from 'styled-components';
import FeatureSection from '../components/FeatureSection';

const Home = () => {
  return (
    <>
      <Header />
      <MainContent>
        <HeroSection>
          <HeroText>
            <h1>ENHANCE YOUR VIDEOS</h1>
            <p>Hashtag Creation Using AI</p>
          </HeroText>
        </HeroSection>
        <FeatureSection
          title="Quality Assurance"
          description="In our pursuit of excellence, we guarantee quality in every aspect of our service. Explore the unique advantages that make us stand out from the rest."
        />
        <FeatureSection
          title="Seamless Uploads"
          description="Effortless Video Uploads. Upload your TikTok videos seamlessly with our user-friendly drag-and-drop interface. Our platform supports various video formats, ensuring a hassle-free experience."
        />
        <FeatureSection
          title="Smart Hashtags"
          description="AI-Powered Hashtag Suggestions. Leverage the power of advanced AI algorithms to analyze your video content and generate the most relevant and trending hashtags. Boost your visibility and engagement on TikTok effortlessly."
        />
        <FeatureSection
          title="Personal Touch"
          description="Customizable Hashtag Lists. Review and personalize your AI-generated hashtags to match your unique style and content goals. Fine-tune your hashtag strategy to maximize your reach and impact on TikTok."
        />
      </MainContent>
      <Footer />
    </>
  );
};

const HeroSection = styled.section`
  background-image: url('/hero.jpg'); // Add your own hero image in the public folder
  background-size: cover;
  background-position: center;
  color: #fff;
  text-align: center;
  padding: 100px 20px;
`;

const HeroText = styled.div`
  background-color: rgba(0, 0, 0, 0.5);
  display: inline-block;
  padding: 20px;
`;

const Section = styled.section`
  padding: 40px 20px;
  text-align: center;
`;

export default Home;
