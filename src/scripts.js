document.addEventListener('DOMContentLoaded', () => {
    fetch('data.txt')
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n');
            const infoDiv = document.getElementById('student-info');

            lines.forEach(line => {
                const div = document.createElement('div');
                div.textContent = line;
                infoDiv.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Error fetching the data:', error);
        });
});
