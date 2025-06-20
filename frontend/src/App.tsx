import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './pages/routes/ProtectedRoute';
import {ROUTES} from './pages/routes/ROUTES.ts'

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path={ROUTES.HOME} element={<LandingPage/>}/>
                <Route path={ROUTES.LOGIN} element={<LoginPage/>}/>
                <Route path={ROUTES.DASHBOARD} element={
                    <ProtectedRoute><Dashboard/></ProtectedRoute>
                }/>
            </Routes>
        </Router>
    );
};

export default App;