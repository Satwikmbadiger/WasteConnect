import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('YOUR_PUBLIC_STRIPE_KEY');

export const createCheckoutSession = async (items) => {
    const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items }),
    });

    if (!response.ok) {
        throw new Error('Failed to create checkout session');
    }

    return response.json();
};

export const redirectToCheckout = async (sessionId) => {
    const stripe = await stripePromise;
    const { error } = await stripe.redirectToCheckout({ sessionId });

    if (error) {
        console.error('Error redirecting to checkout:', error);
    }
};