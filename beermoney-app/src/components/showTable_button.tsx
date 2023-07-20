import React, { useState } from 'react';

const baseURL = 'https://c752tdu4nsjocjzhjzz4hxorze0cdyuv.lambda-url.us-east-2.on.aws/';
const hideURL = 'https://mzwxxmam5v55wv43xejyfohdvq0zmvtg.lambda-url.us-east-2.on.aws/';

const ShowButton: React.FC = () => {
  const [tableData, setTableData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [selectedRows, setSelectedRows] = useState<number[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  const handleClick = () => {
    setIsLoading(true);

    fetch(baseURL, {
      method: 'GET',
      headers: {},
    })
      .then(response => response.json())
      .then(data => {
        const parsedData = JSON.parse(data.body);
        setTableData(parsedData);
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleSort = (columnKey: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig && sortConfig.key === columnKey && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key: columnKey, direction });
  };

  const handleHide = async (rowId: number) => {
    try {
      // Make an API call to update the "hidden" value in the database
      const response = await fetch(hideURL, {
        method: 'POST',
        headers: {},
        body: JSON.stringify({ rowId }), // Include rowId in the request body
      });
      const data = await response.text();
      // Handle the API response to ensure the update was successful
      if (data === 'SUCCESS') {
        console.log(`Row ${rowId} successfully hidden.`);
      } else {
        console.log(`Failed to hide row ${rowId}.`);
      }
    } catch (error) {
      console.error(`Error hiding row ${rowId}.`, error);
    }
  };

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>, rowId: number) => {
    const { checked } = event.target;
    if (checked) {
      setSelectedRows(prevSelectedRows => [...prevSelectedRows, rowId]);
    } else {
      setSelectedRows(prevSelectedRows => prevSelectedRows.filter(id => id !== rowId));
    }
  };

  const handleHideSelected = async () => {
    // Make an array of promises for each selected row's hide API call
    const hidePromises = selectedRows.map(rowId => handleHide(rowId));

    try {
      // Wait for all the hide API calls to finish
      await Promise.all(hidePromises);
      console.log('All selected rows successfully hidden.');

      // Remove the selected rows from the tableData state
      const updatedTableData = tableData.filter(row => !selectedRows.includes(row[0]));
      setTableData(updatedTableData);

      // Clear the selectedRows state
      setSelectedRows([]);
    } catch (error) {
      console.error('Error hiding selected rows.', error);
    }
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    setSearchTerm(value);
  };

  const filteredTableData = React.useMemo(() => {
    if (searchTerm) {
      return tableData.filter(row => {
        return Object.values(row)
          .some(value => String(value).toLowerCase().includes(searchTerm.toLowerCase()));
      });
    }
    return tableData;
  }, [tableData, searchTerm]);

  const sortedTableData = React.useMemo(() => {
    const sortedData = [...filteredTableData];
    if (sortConfig !== null) {
      sortedData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortedData;
  }, [filteredTableData, sortConfig]);

  return (
    <div>
      <button onClick={handleClick} disabled={isLoading}>
        {isLoading ? 'Loading table...' : 'Load Table from DB'}
      </button>
      {selectedRows.length > 0 && (
        <button onClick={handleHideSelected}>Hide Selected</button>
      )}
      <div>
        <label htmlFor="search">Search:</label>
        <input type="text" id="search" value={searchTerm} onChange={handleSearch} />
      </div>
      {tableData.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Select</th>
              <th
                onClick={() => handleSort('0')}
                className={sortConfig && sortConfig.key === '0' ? sortConfig.direction : ''}
              >
                ID
              </th>
              <th
                onClick={() => handleSort('2')}
                className={sortConfig && sortConfig.key === '2' ? sortConfig.direction : ''}
              >
                Title
              </th>
              <th
                onClick={() => handleSort('3')}
                className={sortConfig && sortConfig.key === '3' ? sortConfig.direction : ''}
              >
                Description
              </th>
              <th
                onClick={() => handleSort('4')}
                className={sortConfig && sortConfig.key === '4' ? sortConfig.direction : ''}
              >
                Amount
              </th>
              <th
                onClick={() => handleSort('5')}
                className={sortConfig && sortConfig.key === '5' ? sortConfig.direction : ''}
              >
                Device
              </th>
              <th
                onClick={() => handleSort('6')}
                className={sortConfig && sortConfig.key === '6' ? sortConfig.direction : ''}
              >
                Offerwall
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedTableData.map(row => (
              (row.hidden !== 1) && (
                <tr key={row[0]}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedRows.includes(row[0])}
                      onChange={event => handleCheckboxChange(event, row[0])}
                    />
                  </td>
                  <td>{row[0]}</td>
                  <td>{row[2]}</td>
                  <td>{row[3]}</td>
                  <td>{row[4]}</td>
                  <td>{row[5]}</td>
                  <td>{row[8]}</td>
                </tr>
              )
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ShowButton;
