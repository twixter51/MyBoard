    
    
console.log("Close.js loaded");
function LogoutButton(){
    console.log("HI")

    const exits = document.querySelectorAll(".exits")
    var button = document.getElementById("logout")
    var overlay = document.getElementById("overlay")
    const popups = document.querySelectorAll(".popup")


   
        overlay.classList.add("active");
        
        popups.forEach(pop => {
        pop.classList.add("active");
        });



  

    //loop through till we find an exit clicked.
    exits.forEach(exit=> {

        exit.addEventListener("click", function() {
            console.log(exit.innerHTML)
            if (exit.innerHTML == "Yes"){
                window.location.href = logoutref;
            }
            else{
                overlay.classList.remove("active");
                popups.forEach(pop => {
                    pop.classList.remove("active");
                });
            }
        
            });
            
    });
}
   
