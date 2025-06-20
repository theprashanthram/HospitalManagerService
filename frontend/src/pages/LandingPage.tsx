// components/LandingPage.tsx
import React from 'react';
import {Button, Container, Typography} from '@mui/material';
import {useNavigate} from 'react-router-dom';
import {useDispatch} from 'react-redux';
import type {AppDispatch} from '../store/store';
import {restoreSession} from '../utils/auth';
import {ROUTES} from "./routes/ROUTES.ts";

const LandingPage: React.FC = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch<AppDispatch>();

    const handleLoginClick = async () => {
        const restored = await restoreSession(dispatch);
        if (restored) {
            console.log("Using existing user's credentials to log in")
        }
        navigate(restored ? ROUTES.DASHBOARD : ROUTES.LOGIN);
    };

    return (
        <Container sx={{textAlign: 'center', mt: 8}}>
            <Typography variant="h4" gutterBottom>Welcome to My App</Typography>
            <Button variant="contained" onClick={handleLoginClick}>Login</Button>
        </Container>
    );
};

export default LandingPage;
