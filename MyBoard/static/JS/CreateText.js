

console.log("Creating TEXT");



function createText(text, main){


    console.log("THESE IS THE TEXT IN C TEXT: " + text.content);


    //handle some checks because we are getting either a string or object input
    let textC;
    if (typeof text == "string"){
        textC = text;
    }else{
        textC = text.content;
    }

    //create it
    var textElement = document.createElement("div");
    var profElement = document.createElement("div");
   

    //add classes
    profElement.classList.add("container");
    profElement.classList.add("userProf");
    textElement.classList.add("container");
    textElement.classList.add("textView");

    //this is the text
    textElement.innerHTML = textC.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>'); // Add text content
   
    
    
    profElement.appendChild(textElement);


    let lastDiv = main.lastElementChild?.firstElementChild || main.lastElementChild; // Check if theres a DIV

    // if so lets go through with adding spacing
    if (lastDiv){
        let lastRectTemp = lastDiv.getBoundingClientRect();
       
        //get height 
        heightPos = lastRectTemp.height;
        
        if (heightPos){
            profElement.style.marginTop = (heightPos) + "px";
            profElement.style.display = "block";   // Ensure block display
        }
    }

    return profElement;

}



