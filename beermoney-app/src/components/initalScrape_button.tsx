import React, { useState, ChangeEvent } from 'react';

const baseURL = 'https://jxpokkhf6xnfks3qnbsqmaagim0wunnh.lambda-url.us-east-2.on.aws/';

const ScrapeButton: React.FC = () => {
  const [fsid, setFsid] = useState<string>('');
  const [apiResponse, setApiResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isComplete, setIsComplete] = useState<boolean>(false);

  const handleFsidChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFsid(e.target.value);
  };

  const handleClick = () => {
    // Check if the FSID is empty before making the API request
    if (fsid.trim() === '') {
      alert('Please enter an FSID.'); // You can display an error message to the user
      return; // Prevent the API request if FSID is empty
    }

    setIsLoading(true);

    // Include the FSID as a query parameter in the Lambda URL
    fetch(`${baseURL}?fsid=${fsid}`, {
      method: 'POST',
      headers: {},
    })
      .then((response) => response.text())
      .then((data) => {
        setApiResponse(data);
        console.log('API Response: ', apiResponse);
        if (data === 'SUCCESS') {
          setIsComplete(true);
          setIsLoading(false);
          setTimeout(() => {
            setIsComplete(false);
          }, 60000);
        }
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });
  };

  // Check if fsid is empty to disable the button
  const isButtonDisabled = fsid.trim() === '' || isLoading || isComplete;

  return (
    <div>
      <input
        type="text"
        placeholder="Enter FSID"
        value={fsid}
        onChange={handleFsidChange}
        disabled={isLoading || isComplete}
      />
      <button
        onClick={handleClick}
        disabled={isButtonDisabled}
        className={isComplete ? 'complete-button' : ''}
      >
        {isLoading ? 'Thank you! Please wait..' : isComplete ? 'Complete' : 'Execute Scrape'}
      </button>
    </div>
  );
};

export default ScrapeButton;
