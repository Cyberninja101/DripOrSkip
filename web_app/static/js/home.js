var canvas = document.querySelector("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector('#myVidPlayer');

//w-width,h-height
var w, h;
canvas.style.display = "none";

function retake() {
    document.getElementById("myVidPlayer").style.display = "flex";
    document.getElementById("myCanvas").style.display = "none";
}

function snapshot(){
    // what happens
    // make video player dissapear
    document.getElementById("myVidPlayer").style.display = "none";

    context.fillRect(0, 0, w, h);
    context.drawImage(video, 0, 0, w, h);
    canvas.style.display = "block";



    // attempting download server side
    const dataURL = canvas.toDataURL('image/png');

    fetch('/save_image', {
        method: 'POST',
        body: JSON.stringify({ image: dataURL }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.redirected) {
            // If the response indicates a redirect, navigate to the new location
            window.location.href = response.url;
        } else {
            // Handle other responses as needed
            return response.json();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

window.navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();

            //new
            w = video.videoWidth;
            h = video.videoHeight

            canvas.width = w;
            canvas.height = h;
        };
    })
    .catch(error => {
        alert('You have to enable the mic and the camera');
    });


    document.addEventListener('DOMContentLoaded', function() {
        const hexItems = document.querySelectorAll('.hex-item');

        hexItems.forEach(item => {
            const hexCode = item.getAttribute('data-hex');
            item.style.color = hexCode;  // Apply the hex code as the text color
        });
    });