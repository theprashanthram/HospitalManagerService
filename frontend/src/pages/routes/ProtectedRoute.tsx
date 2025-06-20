// components/ProtectedRoute.tsx
import React, {useEffect, useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import type {RootState, AppDispatch} from '../../store/store';
import {Navigate} from 'react-router-dom';
import {restoreSession} from '../../utils/auth';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({children}) => {
    const token = useSelector((state: RootState) => state.auth.accessToken);
    const dispatch = useDispatch<AppDispatch>();
    const [isLoading, setIsLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuth = async () => {
            if (token) {
                console.log('User authentication is alive')
                setIsAuthenticated(true);
            } else {
                console.log("User is not authenticated, trying to re-auth the user")
                const restored = await restoreSession(dispatch);
                setIsAuthenticated(restored);
            }
            setIsLoading(false);
        };
        checkAuth();
    }, [dispatch, token]);

    if (isLoading) return <div>Loading...</div>;
    return isAuthenticated ? <>{children}</> : <Navigate to="/login"/>;
};

export default ProtectedRoute;
