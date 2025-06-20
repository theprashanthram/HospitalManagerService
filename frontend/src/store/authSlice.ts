import {createSlice, type PayloadAction} from '@reduxjs/toolkit';

interface AuthState {
    accessToken: string | null;
}

const initialState: AuthState = {
    accessToken: localStorage.getItem('access_token'),
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setAccessToken: (state, action: PayloadAction<string>) => {
            state.accessToken = action.payload;
            localStorage.setItem('accessToken', action.payload); // Store in localStorage
        },
        clearAccessToken: (state) => {
            state.accessToken = null;
            localStorage.removeItem('accessToken'); // Remove from localStorage
        },
    },
});

export const {setAccessToken, clearAccessToken} = authSlice.actions;
export default authSlice.reducer;
