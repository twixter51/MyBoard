
function loadData(){
    const isOwner = document.getElementById('is_owner').textContent;

    const textsDataElement = document.getElementById('texts-data');
    const fileDataElement = document.getElementById('files-data');
    
    const main = document.getElementById("MainView");
    let dataStore = []; // we will use this to grab our data from database


    if(isOwner == "false"){
        textEnter1.classList.add("hidden");
        uploadBut.classList.add("hidden");
        fileText.classList.add("hidden");

    }
    
    if (textsDataElement) {
        console.log("TEXT data:", textsDataElement.textContent);
        
        const textsData = JSON.parse(textsDataElement.textContent); 
        console.log("Parsed text Data:", textsData);  
        
        textsData.forEach(text => {

            dataStore.push({
                type: 'text',
                content: text,
                timestamp: text.timestamp,
                id: text.id
            });
            
        });
    }

    if(fileDataElement){
        console.log("File Data:", fileDataElement.textContent);
        const fileData = JSON.parse(fileDataElement.textContent);
        
        fileData.forEach(file => {
            dataStore.push({
                type: 'file',
                key: file.key,
                content: file.content,
                timestamp: file.timestamp,
                id: file.id
            });

        });

    } 

    dataStore.sort((a,b) =>{
        const time1 = new Date(a.timestamp);
        const time2 = new Date(b.timestamp);
        return time1 - time2;
    });
    
    console.log("DATA STORE RUNNING: " + dataStore);


    displayInOrder(dataStore);
    //Datastore ends here
    
    let elements
    let downloadDiv = false
    let downloadMenu
    let downloadBut1
    let removeBut1

    setTimeout(function() {
        grabImage(elements, downloadDiv, downloadMenu, downloadBut1, removeBut1, isOwner);
    }, 1000);

}

