import React, { useState } from 'react';

const baseURL = 'https://us-south.functions.appdomain.cloud/api/v1/web/a50fddb3-8a2d-40f0-83b3-862d10500265/'

const ApiButton: React.FC = () => {
    const [apiResponse, setApiResponse] = useState<any>('');
  const handleClick = () => {
    fetch(baseURL+'src/simple_test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
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
      });
  };

  return (
    <div>
        <button onClick={handleClick}>Click Me</button>
        <div>{apiResponse}</div>
    </div>
  );
};

export default ApiButton;
