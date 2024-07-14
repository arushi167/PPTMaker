// Toggle Profile Menu 
var profile_pic = document.getElementsByClassName("profile-menu-avatar")[0];
var profile_pic_menu = document.getElementsByClassName("chakra-portal")[3].getElementsByClassName("css-iy22zq")[0];

profile_pic.addEventListener("click", () => {
    if (profile_pic_menu.style.visibility == "visible"){
        profile_pic_menu.style.visibility = "hidden"; 
        profile_pic_menu.style.position = "absolute"; 
        profile_pic_menu.style.minWidth = "max-content"; 
        profile_pic_menu.style.inset = "0px auto auto 0px";

        var menuList = profile_pic_menu.getElementsByClassName("css-1i3vl1r")[0];
        menuList.style.transformOrigin = "var(--popper-transform-origin)";
        menuList.style.opacity = "0";
        menuList.style.visibility = "hidden";
        menuList.style.transform = "scale(0.8) translateZ(0px)";

    } else {
        profile_pic_menu.style.visibility = "visible";
        profile_pic_menu.style.minWidth = "max-content";
        profile_pic_menu.style.setProperty("--popper-transform-origin", "top right");
        profile_pic_menu.style.position = "absolute";
        profile_pic_menu.style.inset = "0px 0px auto auto";
        profile_pic_menu.style.margin = "0px";
        profile_pic_menu.style.transform = "translate3d(-23.8625px, 48px, 0px)";
        
        var menuList = profile_pic_menu.getElementsByClassName("css-1i3vl1r")[0];
        menuList.style.transformOrigin = "var(--popper-transform-origin)";
        menuList.style.opacity = "1";
        menuList.style.visibility = "visible";
        menuList.style.transform = "none";
    }
});

// Toggle Present Screen Dropdown
var present_screen_btn = document.getElementsByClassName("css-hcz9sg")[0];
var present_screen_btn_menu = document.getElementsByClassName("chakra-portal")[1].getElementsByClassName("css-iy22zq")[0];

present_screen_btn.addEventListener("click", () => {
    if (present_screen_btn_menu.style.visibility == "visible"){
        present_screen_btn_menu.style.visibility = "hidden"; 
        present_screen_btn_menu.style.position = "absolute"; 
        present_screen_btn_menu.style.minWidth = "max-content"; 
        present_screen_btn_menu.style.inset = "0px auto auto 0px";

        var menuList = present_screen_btn_menu.getElementsByClassName("css-1i3vl1r")[0];
        menuList.style.transformOrigin = "var(--popper-transform-origin)";
        menuList.style.opacity = "0";
        menuList.style.visibility = "hidden";
        menuList.style.transform = "scale(0.8) translateZ(0px)";

    } else {
        present_screen_btn_menu.style.visibility = "visible";
        present_screen_btn_menu.style.minWidth = "max-content";
        present_screen_btn_menu.style.setProperty("--popper-transform-origin", "top right");
        present_screen_btn_menu.style.position = "absolute";
        present_screen_btn_menu.style.inset = "0px 0px auto auto";
        present_screen_btn_menu.style.margin = "0px";
        present_screen_btn_menu.style.transform = "translate3d(-206.587px, 48px, 0px)";
        
        var menuList = present_screen_btn_menu.getElementsByClassName("css-1i3vl1r")[0];
        menuList.style.transformOrigin = "var(--popper-transform-origin)";
        menuList.style.opacity = "1";
        menuList.style.visibility = "visible";
        menuList.style.transform = "none";
    }
});


// Signout Btn
var signout_btn = document.getElementById("menu-list-:r48:-menuitem-:r5k:");
signout_btn.addEventListener("click", ()=>{
    window.location.href="/logout";
});