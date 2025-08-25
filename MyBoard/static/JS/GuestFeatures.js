let guestBanner = document.getElementById("appBanner");
let guestBanner_Text = document.getElementById("appBanner_Text");
let guestBanner_Notify = document.getElementById("appBanner_notify");

if (guestBanner && guestBanner_Text){
  
  guestBanner.style.height = "12px";
  //guestBanner.style.overflow = "hidden";
  guestBanner.style.transition = "height 220ms ease, box-shadow 220ms ease";

  guestBanner_Text.style.opacity = "0";
  guestBanner_Text.style.transform = "translateY(-6px)";
  guestBanner_Text.style.transition = "opacity 180ms ease 40ms, transform 180ms ease 40ms";

  guestBanner.addEventListener("mouseenter", () => {
    guestBanner.style.height = "48px";
    guestBanner.style.boxShadow = "0 10px 24px rgba(0,0,0,.15)";
    guestBanner_Text.style.opacity = "1";
    guestBanner_Text.style.transform = "translateY(0)";
    

  });

  guestBanner.addEventListener("mouseleave", () => {
    guestBanner.style.height = "12px";
    guestBanner.style.boxShadow = "none";
    guestBanner_Text.style.opacity = "0";
    guestBanner_Text.style.transform = "translateY(-6px)";
  });


}