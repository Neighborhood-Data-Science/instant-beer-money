import React, { useState } from 'react';

const baseURL = 'https://c752tdu4nsjocjzhjzz4hxorze0cdyuv.lambda-url.us-east-2.on.aws/'

const ShowButton: React.FC = () => {
    const [apiResponse, setApiResponse] = useState<any>('');
    const [isLoading, setIsLoading] = useState(false);
  const handleClick = () => {
    // Set state to true before making API call
    setIsLoading(true);
    fetch(baseURL, {
      method: 'GET',
      headers: {},
      // Add any necessary request body or parameters
    //   body: JSON.stringify({"name":""}),
    })
      .then(response => response.text())
      .then(data => {
        // Update state with API response
        setApiResponse(data);
      })
      .catch(error => {
        // Handle any errors
        console.error(error);
      })
      .finally(() => {
        // Set state to false after API call is complete
        setIsLoading(false);
      });
    };

  return (
    <div>
        <button onClick={handleClick} disabled={isLoading}>
          {isLoading ? 'Loading table' : 'Load Table from DB'}
          </button>
        <div>{apiResponse}</div>
    </div>
  );
};

export default ShowButton;
