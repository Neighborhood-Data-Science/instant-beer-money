import React, { useState } from 'react';

const baseURL = 'https://jxpokkhf6xnfks3qnbsqmaagim0wunnh.lambda-url.us-east-2.on.aws/';

const ScrapeButton: React.FC = () => {
  const [setApiResponse] = useState<any>(''); // Fix the destructured state setter here
  const [isLoading, setIsLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const handleClick = () => {
    setIsLoading(true);
    fetch(baseURL, {
      method: 'POST',
      headers: {},
    })
      .then(response => response.text())
      .then(data => {
        setApiResponse(data);
        if (data === 'SUCCESS') {
          setIsComplete(true);
          setIsLoading(false);
          setTimeout(() => {
            setIsComplete(false);
          }, 60000);
        }
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  };

  return (
    <div>
      <button
        onClick={handleClick}
        disabled={isLoading || isComplete}
        className={isComplete ? 'complete-button' : ''}
      >
        {isLoading ? 'Scraping...Please Wait.' : isComplete ? 'Complete' : 'Execute Scrape'}
      </button>
    </div>
  );
};

export default ScrapeButton;
