

async function Create(event,file,files,main,currRemoveButs){

    var input = event.target.value 
    console.warn(file);
             
   
    if (input) {

        const formData = new FormData();
        formData.append("text", input);
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfToken) {
            console.error("CSRF token not found!");
            return;
        }
        formData.append('csrfmiddlewaretoken', csrfToken.value); // security

        try {
            const response = await fetch('/messages/', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                
               
                profElement = createText(input, main);
                main.appendChild(profElement);
                event.target.value = ""; // Clear the input field
                
            }else{
                console.error("Error: " + data.error);
            }

        
        } catch (error) {
            console.error('Error:', error);
        }
    
    }

     //exit if no file chosen
    console.log(files.length)
    if(!file){
        console.warn("Texting...");
        return;

    }

    //*************WARN**************************************************
    console.warn("NOW UPLOADING FILE. If code fails please exit this point");
    //***********************************************************
    const waitingImages = document.querySelectorAll(".waitingImages");
    console.warn("TEST IMAGES: " + waitingImages.length);

    if (waitingImages.length > 0){
       
        
        //Upload images first
        for(let i = 0; i < files.length; ++i){
            
            const formData = new FormData();
            
            if(files[i].type.startsWith("image/")){
                formData.append("image", files[i]);
                
                //prompt user
               
            }else if(files[i].type == "video/mp4"){
                formData.append("video", files[i]);
               
            }
             fileText.innerHTML = "Uploading....";
             formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);   
            try {
                const response = await fetch('/upload/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                console.log(data);
                if (data.success) {
                   
                    // Update the UI to show upload success
                    currRemoveButs.forEach(button => {  //now lets remove our waiting images
                        button.click();
                    });
                    setTimeout(() => {
                        fileText.innerHTML = "No file chosen";
                    }, 2000); // wait to notify user just in case?
                }
            } catch (error) {
                console.error('Error uploading image:', error);
                fileText.innerHTML = "ERROR";
            }
        }
      
            
        //lets display to our user then will combine later
        imagesToUpld = Array.from(waitingImages);
        console.warn(imagesToUpld + " IS THE IMAGES ");

        for(let i = 0; i < imagesToUpld.length; ++i) {
            console.log("we are going to put this image now: " + imagesToUpld[i]);
            //throw(new Error("STOP TO TEST"));

                
            if (imagesToUpld[i] instanceof HTMLVideoElement) {
                //video stuff here later

                console.warn("Uploading Video");

                let SrcTest= imagesToUpld[i].src;
                
                let newprofElement = document.createElement("div");
                newprofElement.classList.add("container");
                newprofElement.classList.add("userProf");

                let fileShow = document.createElement("video")
                fileShow.controls = true;
                fileShow.className = "image-container";
              
                fileShow.id = "vid1" + Date.now();
                fileShow.src = SrcTest;
                fileShow.style.borderRadius = 8 + "px";
                fileShow.style.backgroundSize = "contain";
                fileShow.style.backgroundRepeat = "no-repeat";
                fileShow.style.backgroundPosition = "center";
                fileShow.style.backgroundColor = "transparent"; 
                
                

                fileShow.addEventListener('loadedmetadata', function() {
                    //natural dimensions
                    const maxWidth = 800;
                    if (fileShow.videoWidth > maxWidth) {
                        const ratio = fileShow.videoHeight / fileShow.videoWidth;
                        fileShow.width = maxWidth;
                        fileShow.height = maxWidth * ratio;
                    } else {
                        fileShow.width = fileShow.videoWidth;
                        fileShow.height = fileShow.videoHeight;

                    }
                });

                newprofElement.appendChild(fileShow);

                //spacing
                let lastDiv = main.lastElementChild?.firstElementChild; // Check if theres a DIV
                if (lastDiv) {
                    
                    const lastRect = lastDiv.getBoundingClientRect();
                    console.log(lastDiv.getBoundingClientRect())
                    let heightPos = lastRect.height;
                    
                    //check again just in case
                    lastDiv = main.lastElementChild?.firstElementChild; // Check if theres a DIV

                    if (heightPos){
                        newprofElement.style.marginTop = (heightPos) + "px"; // Add some spacing
                        console.log("Here is the new margin: " + newprofElement.style.marginTop);
                        newprofElement.style.display = "block";   // Ensure block display
                    }
                    console.log("SPACED")
                    
                }
                main.appendChild(newprofElement);
            
                
            } else {
                 
                let currentImageSrc = imagesToUpld[i].src;
                //create profile
                let newprofElement = document.createElement("div");
                newprofElement.classList.add("container");
                newprofElement.classList.add("userProf");

                
                const uploadedImg = new Image(); //our new image



                let fileShow = document.createElement("div")
                fileShow.className = "container image-container";
                fileShow.id = "img1" + Date.now();

                uploadedImg.onload = function() {
                    fileShow.style.width = this.naturalWidth + "px";
                    fileShow.style.height = this.naturalHeight + "px";
                    fileShow.style.backgroundImage = `url(${currentImageSrc})`;
                    fileShow.style.backgroundSize = "contain";
                    fileShow.style.backgroundRepeat = "no-repeat";
                    fileShow.style.backgroundPosition = "center";
                    fileShow.style.backgroundColor = "transparent"; 
                    fileShow.style.boxShadow = "none";
                    fileShow.style.borderRadius = 8 + "px";
                    
                    newprofElement.appendChild(fileShow); //append our image with above styles
                    

                    
                    let lastDiv = main.lastElementChild?.firstElementChild; // Check if theres a DIV
                    if (lastDiv) {
                        
                        const lastRect = lastDiv.getBoundingClientRect();
                        console.log(lastDiv.getBoundingClientRect())
                        let heightPos = lastRect.height;
                        
                    
                        //check again just in case
                        lastDiv = main.lastElementChild?.firstElementChild; // Check if theres a DIV

                        
                        if (heightPos){
                            newprofElement.style.marginTop = (heightPos) + "px"; // Add some spacing
                            console.log("Here is the new margin: " + newprofElement.style.marginTop);
                            newprofElement.style.display = "block";   // Ensure block display
                        }
                        console.log("SPACED")

                        
                    }
            
            
                
                    main.appendChild(newprofElement);
                }

                uploadedImg.src = currentImageSrc;

            }
        }


    }



}