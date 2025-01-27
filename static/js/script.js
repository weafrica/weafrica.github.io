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

$(document).ready(function() {
    $('#search-input').on('input', function() {
        let query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: "{{ url_for('news.search_autocomplete') }}",
                method: 'GET',
                data: { query: query },
                success: function(data) {
                    $('#search-results').empty();
                    if (data.results.length > 0) {
                        data.results.forEach(function(result) {
                            if (result.id) {
                                $('#search-results').append('<a href="' + "{{ url_for('news.news_detail', news_id='') }}" + result.id + '" class="list-group-item list-group-item-action">' + result.title + '</a>');
                            }
                        });
                    } else {
                        $('#search-results').append('<p class="list-group-item">No results found</p>');
                    }
                }
            });
        }
    });
});