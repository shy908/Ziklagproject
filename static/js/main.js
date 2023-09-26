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
        this.buttonSubmit();
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
    buttonSubmit(){
        const formButton = document.querySelectorAll('button[type="submit"]');
        if(formButton != undefined){
            formButton.forEach(button => {
                button.addEventListener('click', () => {
                    this.checkFormErrors();
                });
            });
        }
    }
    checkFormErrors(){
        const formError = document.querySelectorAll('.form-error');
        if(formError != undefined){
            formError.forEach(error => {
                if(error.value.length < 0 || error.value == ''){
                    error.classList.toggle('true');
                }
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const dropdownLinks = document.querySelectorAll('.dropdown > a');

    dropdownLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const subMenu = this.nextElementSibling;
            subMenu.classList.toggle('active');
        });
    });
});
;
