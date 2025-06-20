// components/Dashboard.tsx
import React from 'react';
import {useSelector} from 'react-redux';
import type {RootState} from '../store/store';
import {Container, Typography} from '@mui/material';

const Dashboard: React.FC = () => {
    const token = useSelector((state: RootState) => state.auth.accessToken);

    return (
        <Container>
            <Typography variant="h4" sx={{mt: 5}}>Dashboard</Typography>
            <Typography variant="body1">Access Token: {token}</Typography>
        </Container>
    );
};

export default Dashboard;
