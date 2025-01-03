// Add your custom JavaScript here
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready');
});

document.getElementById('showNotificationsLink').addEventListener('click', function(event) {
    event.preventDefault();
    var notificationsBox = document.getElementById('notificationsBox');
    if (notificationsBox.style.display === 'none') {
        notificationsBox.style.display = 'block';
    } else {
        notificationsBox.style.display = 'none';
    }
});

// Function to generate a random color
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Apply random color to the WeAfrica icon
document.getElementById('weafrica-icon').style.color = getRandomColor();