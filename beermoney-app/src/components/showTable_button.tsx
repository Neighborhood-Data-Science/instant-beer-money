import React, { useState } from 'react';

const baseURL = 'https://c752tdu4nsjocjzhjzz4hxorze0cdyuv.lambda-url.us-east-2.on.aws/';

const ShowButton: React.FC = () => {
  const [tableData, setTableData] = useState<any[]>([]); // Provide an initial empty array as default value
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    // Set state to true before making API call
    setIsLoading(true);

    fetch(baseURL, {
      method: 'GET',
      headers: {},
    })
      .then(response => response.json())
      .then(data => {
        // Parse the JSON response
        const parsedData = JSON.parse(data.body);
        // Update state with parsed data
        setTableData(parsedData);
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
        {isLoading ? 'Loading table...' : 'Load Table from DB'}
      </button>
      {tableData.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              {/* Add more column headers as needed */}
            </tr>
          </thead>
          <tbody>
            {tableData.map(row => (
              <tr key={row[0]}>
                <td>{row[0]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                {/* Map the remaining columns to <td> elements */}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ShowButton;
