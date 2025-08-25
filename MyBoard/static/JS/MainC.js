

async function Create(event,file,files,main,currRemoveButs){

    var input = event.target.value 
 
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
                
                profElement = createText(input, main); // call function from Static/Js/CreateText
               
                profElement.dataset.id = data.id;
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
    console.log("Length of waiting files: " + files.length)
    if(!file){
        console.warn("Texting...");
    
    }

    //*************WARN**************************************************
    console.warn("Trying to upload files if there are any");
    //***********************************************************
    const waitingImages = document.querySelectorAll(".waitingImages");
    console.warn("TEST IMAGES: " + waitingImages.length);
    const storeFile = Array.from(document.querySelectorAll(".waitingImages"));

    if (waitingImages.length > 0){

        

        //Upload images first
        for(let i = 0; i < files.length; ++i){

           

           
           console.log(files[i].name);        
            
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
                    
              
                    let add = false; // are we going to remove or add data
                    Calculate_UserStorage(data.size, add); // call to update user storage
                    
                    //match id's so later We can delete em 
                    const matchingEl = storeFile[i];
                    if (matchingEl) {
                        matchingEl.dataset.id = data.id;   
                    }
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

        console.log(imagesToUpld.length)
        console.log(files.length)
        console.warn(imagesToUpld + " IS THE IMAGES ");

            

        for(let i = 0; i < imagesToUpld.length; ++i) {
            console.log("we are displaying: " + imagesToUpld[i]);
            let file = await createDom(imagesToUpld[i], main);
            
            main.appendChild(file);
          
        }

    }

    main.scrollTo({
        top: main.scrollHeight,
        behavior: 'smooth'
    });


    let elements
    let downloadDiv = false
    let downloadMenu
    let downloadBut1
    let removeBut1
    const isOwner = document.getElementById('is_owner').textContent;

    setTimeout(function() {
        grabImage(elements, downloadDiv, downloadMenu, downloadBut1, removeBut1, isOwner);
    }, 1000);


}