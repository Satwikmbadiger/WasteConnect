// Function to get current location and convert to address
async function getCurrentLocation() {
    const addressInput = document.getElementById('address');
    
    // Show loading state
    addressInput.value = 'Getting location...';
    addressInput.disabled = true;

    try {
        // Get current position
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });

        const { latitude, longitude } = position.coords;

        // Use Nominatim for reverse geocoding
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`
        );

        if (!response.ok) {
            throw new Error('Failed to get address');
        }

        const data = await response.json();
        
        // Format the address
        const address = data.display_name;
        
        // Update the input field
        addressInput.value = address;
        addressInput.disabled = false;

    } catch (error) {
        console.error('Error getting location:', error);
        addressInput.value = '';
        addressInput.disabled = false;
        alert('Could not get your location. Please enter address manually.');
    }
}

// Function to handle form submission
async function schedulePickup(event) {
    event.preventDefault();
    
    const successAlert = document.getElementById('successAlert');
    const errorAlert = document.getElementById('errorAlert');
    const form = document.getElementById('pickupForm');
    
    // Hide any existing alerts
    successAlert.style.display = 'none';
    errorAlert.style.display = 'none';

    try {
        const formData = {
            pickupDate: document.getElementById('pickup_date').value,
            address: document.getElementById('address').value
        };

        const response = await fetch('/wastepickup/addSchedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to schedule pickup');
        }

        // Check if we received a pickup_id and message
        if (data.pickup_id) {
            successAlert.textContent = data.message || 'Pickup scheduled successfully!';
            successAlert.style.display = 'block';
            
            // Show success message briefly before redirecting
            setTimeout(() => {
                // Navigate to the getSchedule route with the pickup_id
                window.location.href = '/wastepickup/getSchedule/' + data.pickup_id;
            }, 1500); // Wait 1.5 seconds before redirecting
        } else {
            throw new Error('No pickup ID received from server');
        }

    } catch (error) {
        console.error('Error:', error);
        errorAlert.textContent = error.message;
        errorAlert.style.display = 'block';
    } finally {
        // Hide loading and re-enable submit button
        loading.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Add location button when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pickupForm');
    const addressInput = document.getElementById('address');
    
    // Add a button next to the address input
    const locationButton = document.createElement('button');
    locationButton.type = 'button';
    locationButton.textContent = '📍 Get My Location';
    locationButton.className = 'location-btn';
    locationButton.onclick = getCurrentLocation;
    
    // Insert button after address input
    addressInput.parentNode.insertBefore(locationButton, addressInput.nextSibling);
});