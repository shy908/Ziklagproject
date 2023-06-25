window.addEventListener('DOMContentLoaded', () => {
    console.log('Main script has been loaded');
    try{
        new Scripts();
    }catch(e){}
});

class Scripts{
    constructor(){
        this.init();
    }
    init(){
        this.animateBurgerMenu();
        this.copyRightYear();
    }
    animateBurgerMenu(){

        const burgerMenu = document.querySelector('.burger-menu');

        burgerMenu.addEventListener('click', () => {
            let navSibling = burgerMenu.nextElementSibling;
            if(navSibling.style.maxHeight){
                navSibling.style.maxHeight = null;
            }else{
                navSibling.style.maxHeight = `${navSibling.scrollHeight}px`;
            }
        });
    }
    copyRightYear(){
        const copyright = document.querySelector('footer .copyright span');
        if(copyright != undefined){
            let year = new Date().getFullYear();
            copyright.innerHTML = (year > 2023) ? `&copy; 2023 - ${year} | JRM Archive` : `&copy; ${year} | JRM Archive` ;
        }
    }
}