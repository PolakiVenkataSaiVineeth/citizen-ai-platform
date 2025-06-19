async function submitFeedback() {
    const feedback = document.getElementById('feedback').value;
    const button = document.querySelector('button');
    const successMessage = document.getElementById('feedback-success');
    
    if (!feedback.trim()) {
        alert('Please enter your feedback');
        return;
    }
    
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
    
    try {
        const response = await fetch('/submit-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ feedback })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('feedback').value = '';
            successMessage.style.display = 'block';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 3000);
        } else {
            throw new Error(data.error || 'Error submitting feedback');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    } finally {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Feedback';
    }
}

// Dashboard charts
if (window.location.pathname === '/dashboard') {
    fetchDashboardData();
}

async function fetchDashboardData() {
    try {
        const response = await fetch('/api/feedback');
        const data = await response.json();
        
        createSentimentChart(data);
        createCategoriesChart(data);
        updateRecentFeedback(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

function createSentimentChart(data) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [30, 50, 20], // Replace with actual data
                backgroundColor: ['#00c853', '#ffd600', '#ff1744']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createCategoriesChart(data) {
    const ctx = document.getElementById('categoriesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Category 1', 'Category 2', 'Category 3'], // Replace with actual categories
            datasets: [{
                label: 'Feedback Count',
                data: [12, 19, 8], // Replace with actual data
                backgroundColor: '#2962ff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function updateRecentFeedback(data) {
    const container = document.getElementById('recent-feedback');
    // Add recent feedback items here
}