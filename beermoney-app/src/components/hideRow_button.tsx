import React from 'react';

interface HideButtonProps {
  rowId: number;
  onHide: (rowId: number) => void;
  handleHideSelected: () => void; // Added handleHideSelected function
}

const HideButton: React.FC<HideButtonProps> = ({ rowId, onHide, handleHideSelected }) => {
  const handleHide = () => {
    onHide(rowId);
  };

  return (
    <>
      <button onClick={handleHide}>Hide</button>
      <button onClick={handleHideSelected}>Hide Selected</button> {/* Added button for hiding selected rows */}
    </>
  );
};

export default HideButton;
