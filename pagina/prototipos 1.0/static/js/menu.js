const nav=document.querySelector(".nav");
const log=document.querySelector(".logo");

    window.addEventListener("scroll",function(){
        nav.classList.toggle("active",window.scrollY >0)
        log.classList.toggle("active",window.scrollY >0)
    })
