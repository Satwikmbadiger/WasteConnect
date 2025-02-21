import React, { createContext, useContext, useState, useEffect } from 'react';
import { firebaseAuth } from '../services/firebase';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const unsubscribe = firebaseAuth.onAuthStateChanged(user => {
            setCurrentUser(user);
            setLoading(false);
        });
        return unsubscribe;
    }, []);

    const login = async (email, password) => {
        return await firebaseAuth.signInWithEmailAndPassword(email, password);
    };

    const logout = async () => {
        return await firebaseAuth.signOut();
    };

    const register = async (email, password) => {
        return await firebaseAuth.createUserWithEmailAndPassword(email, password);
    };

    const value = {
        currentUser,
        login,
        logout,
        register,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};