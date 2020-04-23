let constraintObj = { 
    audio: true,
    video: { 
        facingMode: "user", 
        width: { min: 640, ideal: 1280, max: 1920 },
        height: { min: 480, ideal: 720, max: 1080 } 
    } 
}; 


//handle older browsers that might implement getUserMedia in some way
if (navigator.mediaDevices === undefined) {
    navigator.mediaDevices = {};
    navigator.mediaDevices.getUserMedia = function(constraintObj) {
        let getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        if (!getUserMedia) {
            return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
        }
        return new Promise(function(resolve, reject) {
            getUserMedia.call(navigator, constraintObj, resolve, reject);
        });
    }
}else{
    navigator.mediaDevices.enumerateDevices()
    .then(devices => {
        devices.forEach(device=>{
            console.log(device.kind.toUpperCase(), device.label);
            //, device.deviceId
        })
    })
    .catch(err=>{
        console.log(err.name, err.message);
    })
}



function openModal() {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('fade').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('fade').style.display = 'none';
}

function btnStopVisiblity(x)
{
    if (x == 0)
    {
        document.getElementById('btnStop').style.visibility = 'visible';
    }
}




navigator.mediaDevices.getUserMedia(constraintObj)
.then(function(mediaStreamObj) {
    //connect the media stream to the first video element
    let video = document.querySelector('video');
   
    if ("srcObject" in video) {
        video.srcObject = mediaStreamObj;
        
    } else {
        //old version
        video.src = window.URL.createObjectURL(mediaStreamObj);
    }
    
    video.onloadedmetadata = function(ev) {
        //show in the video element what is being captured by the webcam
        //video.play();
    };
    
    //add listeners for saving video/audio
    let start = document.getElementById('btnStart');
    let stop = document.getElementById('btnStop');
    let vidSave = document.getElementById('vid2');
    let mediaRecorder = new MediaRecorder(mediaStreamObj);
    let chunks = [];

  
    

    start.addEventListener('click', (ev)=>{
        mediaRecorder.start();
        video.play();
        
        var counter = 300;
        
        setInterval(function() {
        counter--;
        var realTime = parseInt(counter / 60) + ':' + (counter % 60);
        if (counter >= 0) 
        {
            span = document.getElementById("count");
            span.innerHTML = realTime;
        }

        if (counter === 0) 
        {
            mediaRecorder.stop();
            //alert('Video Record Finish!');
            clearInterval(counter);
            openModal();
        }

        }, 1000);
        
        console.log(mediaRecorder.state);
    })
    stop.addEventListener('click', (ev)=>{
        mediaRecorder.stop();
        
        //alert('Video Record Stopped!');
        //clearInterval(counter);
        console.log(mediaRecorder.state);
        //document.getElementById('results').innerHTML = '';
        openModal();
    });
    mediaRecorder.ondataavailable = function(ev) {
        chunks.push(ev.data);
        //console.log(ev.data);
    }
    mediaRecorder.onstop = (ev)=>{
        let blob = new Blob(chunks, { 'type' : 'video/mp4;' });
        chunks = [];
        
        // let videoURL = window.URL.createObjectURL(blob);
        // vidSave.src = videoURL;
        // console.log(blob);

        

        var formData = new FormData();
        formData.append('video', blob);
        
        // Execute the ajax request, in this case we have a very simple PHP script
        // that accepts and save the uploaded "video" file
        xhr('/recordVideo', formData, function (fName)
        {
            console.log("Video succesfully uploaded !");
            window.location.href = "/watchVideo"; 
        });

        // Helper function to send 
        function xhr(url, data, callback) 
        {
            var request = new XMLHttpRequest();
            request.onreadystatechange = function () 
            {
                if (request.readyState == 4 && request.status == 200) 
                {
                    callback(location.href + request.responseText);
                }
               
            };
            request.open('POST', url);
            request.send(data);
        }
        
    }
    
})
.catch(function(err) { 
    console.log(err.name, err.message); 
});

/*********************************
getUserMedia returns a Promise
resolve - returns a MediaStream Object
reject returns one of the following errors
AbortError - generic unknown cause
NotAllowedError (SecurityError) - user rejected permissions
NotFoundError - missing media track
NotReadableError - user permissions given but hardware/OS error
OverconstrainedError - constraint video settings preventing
TypeError - audio: false, video: false
*********************************/
