"use client";

import styled from 'styled-components';
import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';

const UploadContainer = styled.div`
    display: flex;
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

const UploadImage = styled.div`
    width: 100px;
    height: 200px;
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
    cursor: pointer;
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
    &:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
`;

const DeleteButton = styled.button`
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: red;
    color: white;
    border: none;
    border-radius: 50%;
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
`;

const UploadButton = () => {
    const fileInputRef = useRef(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [videoUrl, setVideoUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleAddClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setVideoUrl(URL.createObjectURL(file));
    };

    const handleUploadClick = () => {
        if (!selectedFile) {
            alert('Please select a video first');
            return;
        }
    
        setLoading(true);
        const formData = new FormData();
        formData.append('video', selectedFile);
    
        console.log('Starting fetch request to upload video...');
    
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            console.log('Fetch request completed. Checking response...');
            setLoading(false); // Ensure loading state is reset
            if (!response.ok) {
                console.error('Response not OK:', response);
                return response.text().then(errorText => {
                    console.error('Error response text:', errorText);
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Response JSON:', data);
            if (data.top_tags) {
                alert('Video uploaded successfully');
    
                // Navigate to the ResultsPage with the videoTags and audioTags
                const query = new URLSearchParams({
                    topTags: JSON.stringify(data.top_tags),
                }).toString();
                router.push(`/results?${query}`);
            } else {
                console.error('Unexpected response structure:', data);
                alert('Unexpected response structure received from server.');
            }
        })
        .catch(error => {
            setLoading(false);  // Ensure loading is set to false in case of error
            console.error('Error in fetch operation:', error);
            alert('Error uploading video: ' + error.message);
        });
    };
    
    const handleDeleteClick = () => {
        setSelectedFile(null);
        setVideoUrl(null);
        fileInputRef.current.value = null; // Reset the file input value
    };

    return (
        <UploadContainer>
            <UploadImage>
                {videoUrl ? (
                    <>
                        <video width="100" height="200" controls>
                            <source src={videoUrl} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                        <DeleteButton onClick={handleDeleteClick}>×</DeleteButton>
                    </>
                ) : (
                    <UploadIcon onClick={handleAddClick}>+</UploadIcon>
                )}
                <input
                    type="file"
                    accept="video/*"
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                    onChange={handleFileChange}
                />
            </UploadImage>
            <UploadButtonStyled onClick={handleUploadClick} disabled={loading}>
                {loading ? 'Uploading...' : 'Upload Video'}
            </UploadButtonStyled>
        </UploadContainer>
    );
};

export default UploadButton;