async function createDom(file, main){

   
    let fileShow = false;
    let overlay = false; //for videos
    let SrcTest = file.src || file.content;
    let newprofElement = document.createElement("div");
    let type;

    if(file instanceof HTMLVideoElement || file?.key == "video"){
        type = "video";
    }else{
        type = "image";
    }

    newprofElement.classList.add("container");
    newprofElement.classList.add("userProf");


    if (type == "video") {
        //video stuff here later
        console.warn("Uploading Video");

        //define
        fileShow = document.createElement("video");

        await new Promise(resolve =>{


            if (!SrcTest.startsWith('blob:')) {
               
                console.log("Converting file path to blob URL:", SrcTest);
                
                // Fetch the video file and convert to blob
                fetch(SrcTest)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Failed to fetch video: ${response.status} ${response.statusText}`);
                        }
                        return response.blob();
                    })
                    .then(blob => {
                        
                        const blobUrl = URL.createObjectURL(blob);
                        
                    
                        setupVideoWithSource(blobUrl);
                    })
                    .catch(error => {
                        console.error("Error creating blob URL:", error);
                        setupVideoWithSource(SrcTest);
                    });
            } else {
                
                console.log("Using existing blob URL");
                setupVideoWithSource(SrcTest);
            }
            

            function setupVideoWithSource(src){
                overlay = document.createElement("div");
                fileShow.src = src;
                fileShow.controls = true;
                fileShow.id = "vid1" + Date.now();
                fileShow.style.borderRadius = "8px";
                fileShow.style.backgroundColor = "transparent";


                fileShow.addEventListener('loadedmetadata', function() {
                    // Set dimensions based on video size
                    fileShow.width = 500;
                    fileShow.height = 350;
                    //set our overlay to simulate an image
                    overlay.style.width = 500;
                    overlay.style.height = 350;
                    overlay.style.position = "relative";

                    overlay.appendChild(fileShow);
                    newprofElement.appendChild(overlay);
                    resolve();
                });

                //in case error happens
                fileShow.addEventListener('error', function() {
                    console.error("Video error code:", fileShow.error?.code);
                    console.error("Video error message:", fileShow.error?.message);
                    resolve(); 
                });

            }
            
      
           



        })
        

        

        //spacing
        applySpacing(newprofElement, main);

        
    } else if(type == "image") {
           
        
        await new Promise(resolve =>  {
                  
            const uploadedImg = new Image(); //our new image

            fileShow = document.createElement("div")
            fileShow.className = "container image-container";
            fileShow.id = "img1" + Date.now();

            uploadedImg.onload = function() {
                fileShow.style.width = this.naturalWidth + "px";
                fileShow.style.height = this.naturalHeight + "px";
                fileShow.style.backgroundImage = `url(${SrcTest})`;
                fileShow.style.backgroundSize = "contain";
                fileShow.style.backgroundRepeat = "no-repeat";
                fileShow.style.backgroundPosition = "center";
                fileShow.style.backgroundColor = "transparent"; 
                fileShow.style.boxShadow = "none";
                
                resolve(); 

        
            };
            
            newprofElement.appendChild(fileShow); //append our image with above styles
            
           //spacing
           applySpacing(newprofElement, main);

            uploadedImg.src = SrcTest; 

        })
            

        
    }

    // now lets confirm with our backend and append a unique id.
    if (!file.id && file.dataset?.id) {
        newprofElement.dataset.id = file.dataset.id
    }else{
        newprofElement.dataset.id = file.id;
    }
   
   

    return newprofElement;

}



function applySpacing(element, main){
    let lastDiv = main.lastElementChild?.firstElementChild 
    // Check if theres a DIV
     if (lastDiv) {
            
        const lastRect = lastDiv.getBoundingClientRect();
        console.log(lastDiv.getBoundingClientRect())
        let heightPos = lastRect.height;

        if (heightPos){
            element.style.marginTop = (heightPos) + "px"; // Add some spacing
            console.log("Here is the new margin: " + element.style.marginTop);
            element.style.display = "block";   // Ensure block display
        }    
        
    }
}


