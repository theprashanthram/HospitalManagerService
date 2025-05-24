// src/pages/Login/LoginPage.tsx
import React, { useState } from 'react';
import InputField from "../components/InputField/InputField";
import Button from '../components/Button/Button';
import type {LoginFormState} from '../types/formTypes';
import {
  Box,
  Typography,
  Paper,
} from '@mui/material';

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState<LoginFormState>({
    email: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = () => {
    console.log('Logging in with:', formData);
  };

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
      }}
    >
      <Paper
        elevation={3}
        sx={{
          padding: 4,
          width: '100%',
          maxWidth: '400px', // ensures it doesn't stretch too wide
          boxSizing: 'border-box',
        }}
      >
        <Typography variant="h4" align="center" gutterBottom>
          Login
        </Typography>
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
        >
          <InputField
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          <InputField
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          <Button text="Login" type="submit" onClick={handleLogin} />
        </Box>
      </Paper>
    </Box>
  );
};

export default LoginPage;
