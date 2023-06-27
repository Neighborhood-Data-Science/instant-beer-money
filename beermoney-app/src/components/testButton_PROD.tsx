import React, { useState } from 'react';

const ApiButton: React.FC = () => {
    const [apiResponse, setApiResponse] = useState<any>('');
  const handleClick = () => {
    fetch('${source}src/simple_test', {
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
