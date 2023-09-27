import React, { useState, ChangeEvent } from 'react';

const baseURL = 'https://jxpokkhf6xnfks3qnbsqmaagim0wunnh.lambda-url.us-east-2.on.aws/';

const ScrapeButton: React.FC = () => {
  const [fsid, setFsid] = useState<string>('');
  const [apiResponse, setApiResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isComplete, setIsComplete] = useState<boolean>(false);

  const handleFsidChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    // Check if the new value is numeric (contains only digits)
    if (/^\d*$/.test(newValue)) {
      setFsid(newValue);
    }
  };

  const handleClick = () => {
    // Check if the FSID is empty or not numeric before making the API request
    if (fsid.trim() === '' || !/^\d*$/.test(fsid)) {
      alert('Please enter a valid numeric FSID.');
      return;
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

  // Check if fsid is empty or not numeric to disable the button
  const isButtonDisabled = fsid.trim() === '' || !/^\d*$/.test(fsid) || isLoading || isComplete;

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
