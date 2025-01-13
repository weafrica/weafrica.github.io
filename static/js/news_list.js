document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    var readMoreLinks = document.querySelectorAll('.read-more-link');
    readMoreLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('Read More link clicked');
            var articleId = this.getAttribute('data-article-id');
            console.log('Article ID:', articleId);
            var articleBody = document.getElementById('article-body-' + articleId);
            if (articleBody) {
                console.log('Article body found:', articleBody);
                if (articleBody.style.display === 'none' || articleBody.style.display === '') {
                    articleBody.style.display = 'block';
                    this.textContent = 'Read Less';
                    console.log('Article body displayed');
                } else {
                    articleBody.style.display = 'none';
                    this.textContent = 'Read More';
                    console.log('Article body hidden');
                }
            } else {
                console.error('Article body not found for ID:', articleId);
            }
        });
    });
});