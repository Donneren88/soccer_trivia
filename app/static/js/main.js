document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        console.log('WebSocket connected');
    });

    socket.on('update_score', data => {
        document.getElementById('score').innerText = data.score;
    });

    // Additional JS for gameplay interactivity
});
