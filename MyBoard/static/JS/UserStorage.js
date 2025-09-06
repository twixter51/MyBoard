let storageLeft = JSON.parse(document.getElementById("storage_left").textContent);
//update storage
updateStorageView(storageLeft)

async function Calculate_UserStorage(value, add){

    storageLeft = JSON.parse(document.getElementById("storage_left").textContent);

    if(value > storageLeft){
        return
    }

    if(!add){
        storageLeft -= value;
    }else{
        storageLeft += value;
    }
    

    let formData = new FormData();
    formData.append("update_storage", storageLeft)
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);  
    
   
    try{
        let response =  await fetch("/update_user/", { method: 'POST', body: formData,});
        const data = await response.json();

        if (data.success){
            console.warn("Updated User Storage")
            
            updateStorageView(data.storage_left)

        }
    }catch(error){
        console.error(error)
    }


}


function updateStorageView(storageLeft){
    let updateBar1 = document.getElementById("userstorage_bar")
    let updateView1 = document.getElementById("userstorage_viewer")

    let usedStorage = ((25*1024) - storageLeft).toFixed(2)
    let is_premium = JSON.parse(document.getElementById("is_premium").textContent);
    let size = "MB"
    let max = 25
    let displaySize = ((25*1024) -  storageLeft).toFixed(2)
    let displaySizeP = ((((25*1024) - storageLeft) / (25*1024)))

    //place holder for when user uploads more than 99MB
    if(usedStorage > 100){
        size = "GB"
        while (usedStorage >= 10){
            usedStorage = usedStorage / 10
        }    
    }
    
  
    if(is_premium){
        max = "Unlimited"
        displaySize = ((1e9) -  storageLeft).toFixed(2)
        displaySizeP = ((((1e9) - storageLeft) / (1e9))).toFixed(2)
    }

    //update storage
    updateBar1.style.width = storageLeft / (25*1024) + "%"
    updateView1.innerHTML =  displaySize + " " + size + " of " +  max +  " GB used (" + displaySizeP + "%)";
}