import React, { useState, } from 'react';
import {
    Container, Paper, Typography, TextField, Button,
    InputAdornment, IconButton, Box
} from '@mui/material';
import { Email, Lock, Visibility, VisibilityOff } from '@mui/icons-material';
import { useDispatch, } from 'react-redux';
import type {AppDispatch,} from "../store/store";
import { setAccessToken } from '../store/authSlice';
import { useNavigate } from 'react-router-dom';
import { type ObtainAuthTokenRequest } from 'hospital-manager-client';
import { backendClient } from "../utils/backendClient";
import { ROUTES } from './routes/ROUTES.ts';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const dispatch = useDispatch<AppDispatch>();
    const navigate = useNavigate();

    const isFormValid = email && password && /\S+@\S+\.\S+/.test(email);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setErrorMessage(null);
        try {
            const request: ObtainAuthTokenRequest = { email, password };
            const res = await backendClient.auth.obtainAuthToken(request);
            dispatch(setAccessToken(res.access_token));
            navigate(ROUTES.DASHBOARD);
        } catch (error) {
            console.error('Login failed', error);
            setErrorMessage('Invalid email or password. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
                <Typography variant="h5" gutterBottom>
                    Login
                </Typography>
                <Box component="form" onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        required
                        margin="normal"
                        label="Email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <Email />
                                </InputAdornment>
                            ),
                        }}
                    />
                    <TextField
                        fullWidth
                        required
                        margin="normal"
                        label="Password"
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <Lock />
                                </InputAdornment>
                            ),
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        onClick={() => setShowPassword(!showPassword)}
                                        edge="end"
                                        aria-label="toggle password visibility"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />
                    {errorMessage && (
                        <Typography color="error" sx={{ mt: 2 }}>
                            {errorMessage}
                        </Typography>
                    )}
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3 }}
                        disabled={!isFormValid || loading}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default LoginPage;
