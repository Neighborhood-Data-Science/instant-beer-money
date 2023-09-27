import React, { useState, useEffect } from 'react';

const baseURL = 'https://c752tdu4nsjocjzhjzz4hxorze0cdyuv.lambda-url.us-east-2.on.aws/';
const hideURL = 'https://mzwxxmam5v55wv43xejyfohdvq0zmvtg.lambda-url.us-east-2.on.aws/';

const ShowButton: React.FC = () => {
  const [tableData, setTableData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [selectedRows, setSelectedRows] = useState<number[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [fsid, setFsid] = useState<string>(''); // New state for user input

  // New useEffect to handle API call when fsid changes
  useEffect(() => {
    if (fsid.trim() === '' || !/^\d*$/.test(fsid)) {
      // Optionally show an error message to the user if fsid is empty or not numeric
      return;
    }

    setIsLoading(true);

    fetch(`${baseURL}?fsid=${fsid}`, {
      method: 'GET',
      headers: {},
    })
      .then((response) => response.json())
      .then((data) => {
        const parsedData = JSON.parse(data.body);
        setTableData(parsedData);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [fsid]);

  const handleClick = () => {
    // Your existing code to load data from the server


  // Rest of your component remains the same

  return (
    <div>
      <button onClick={handleClick} disabled={isLoading}>
        {isLoading ? 'Loading table...' : 'Load Table from DB'}
      </button>
      {/* Input field for FSID */}
      <input
        type="text"
        placeholder="Enter FSID"
        value={fsid}
        onChange={(e) => setFsid(e.target.value)}
        disabled={isLoading}
      />
      {selectedRows.length > 0 && (
        <button onClick={handleHideSelected}>Hide Selected</button>
      )}
      <div>
        <label htmlFor="search">Search:</label>
        <input type="text" id="search" value={searchTerm} onChange={handleSearch} />
      </div>
      {tableData.length > 0 && (
        <table>
          {/* Rest of your table rendering code */}
        </table>
      )}
    </div>
  );
};

export default ShowButton;
