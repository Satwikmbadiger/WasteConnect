import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust the base URL as needed

export const schedulePickup = async (pickupData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/waste/schedule`, pickupData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const getEcoPoints = async (userId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/eco-points/${userId}`);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const getMarketplaceItems = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/marketplace`);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const purchaseItem = async (itemId, userId) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/marketplace/purchase`, { itemId, userId });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const trackRecycling = async (recyclingData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/waste/recycle`, recyclingData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};