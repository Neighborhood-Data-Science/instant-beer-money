import React from 'react';

interface HideButtonProps {
  rowId: number;
  onHide: (rowId: number) => void;
}

const HideButton: React.FC<HideButtonProps> = ({ rowId, onHide }) => {
  const handleHide = () => {
    onHide(rowId);
  };

  return (
    <button onClick={handleHide}>Hide</button>
  );
};

export default HideButton;
