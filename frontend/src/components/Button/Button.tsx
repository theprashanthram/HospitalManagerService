import React from 'react';
import { Button as MUIButton } from '@mui/material';

type ButtonProps = {
  text: string;
  onClick: () => void;
  type?: 'button' | 'submit';
};

const Button: React.FC<ButtonProps> = ({ text, onClick, type = 'button' }) => {
  return (
    <MUIButton
      variant="contained"
      color="primary"
      onClick={onClick}
      type={type}
      fullWidth
      sx={{ marginTop: 2 }}
    >
      {text}
    </MUIButton>
  );
};

export default Button;
