import type {AppDispatch} from '../store/store';
import {setAccessToken} from '../store/authSlice';
import { backendClient } from "./backendClient.ts";

export const restoreSession = async (dispatch: AppDispatch): Promise<boolean> => {
    /*
    Restore session with refresh token if available in the HTTP cookie
     */
    try {
        const response = await backendClient.auth.refreshAuthToken()
        if (response.access_token) {
            dispatch(setAccessToken(response.access_token));
            console.log('Session restored using refresh token')
            return true
        } else {
            console.log('Session was not restored')
            return false
        }
    } catch (error) {
        console.error('Session could not be restored with' +
            ' refresh token for access token', error)
        return false;
    }
};