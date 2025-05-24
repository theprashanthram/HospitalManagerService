import React from 'react';
import { TextField } from '@mui/material';

type InputFieldProps = {
  label: string;
  type: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const InputField: React.FC<InputFieldProps> = ({ label, type, name, value, onChange }) => {
  return (
    <TextField
      label={label}
      type={type}
      name={name}
      value={value}
      onChange={onChange}
      fullWidth
      margin="normal"
      variant="outlined"
    />
  );
};

export default InputField;
