import React, { useState } from 'react';
import HideButton from './hideRow_button';

const baseURL = 'https://c752tdu4nsjocjzhjzz4hxorze0cdyuv.lambda-url.us-east-2.on.aws/';

const ShowButton: React.FC = () => {
  const [tableData, setTableData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

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

  const handleHide = (rowId: number) => {
    // Update the "hidden" value of the corresponding row in the tableData state
    const updatedTableData = tableData.map(row => {
      if (row[0] === rowId) {
        return { ...row, hidden: 1 };
      }
      return row;
    });
    setTableData(updatedTableData);

    // Make an API call to update the "hidden" value in the database
    // You can pass the rowId as a parameter in the API call

    // Handle the API response to ensure the update was successful

    // Update the tableData state with the updated row data after a successful response
    // setTableData(updatedDataFromResponse);
  };

  const sortedTableData = React.useMemo(() => {
    const sortedData = [...tableData];
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
  }, [tableData, sortConfig]);

  return (
    <div>
      <button onClick={handleClick} disabled={isLoading}>
        {isLoading ? 'Loading table...' : 'Load Table from DB'}
      </button>
      {tableData.length > 0 && (
        <table>
          <thead>
            <tr>
            <th
                onClick={() => handleSort('0')}
                className={sortConfig && sortConfig.key === '5' ? sortConfig.direction : ''}
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
                Hidden
              </th>
              <th
                onClick={() => handleSort('8')}
                className={sortConfig && sortConfig.key === '8' ? sortConfig.direction : ''}
              >
                Offerwall
              </th>
              <th>Action</th> {/* Add a new column for the action button */}
              {/* Add more column headers as needed */}
            </tr>
          </thead>
          <tbody>
            {sortedTableData.map(row => (
              <tr key={row[0]}>
                <td>{row[0]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
                <td>{row[6]}</td>
                <td>{row[8]}</td>
                <td>
                {row.hidden !== 1 && (
                    <HideButton rowId={row[0]} onHide={handleHide} />
                  )}
                </td>
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
