// play background video after load

document.querySelector("video").src = "./images/briquettes.mp4"
  

// controlling the hero briefs

const heroBriefs = document.querySelectorAll("[data-briefs]")

const activeBrief = document.querySelector("[data-active]") 


let startIndex = 0
setInterval( () => {   
    
    const activeBrief = document.querySelector("[data-active]") 
      
    delete activeBrief.dataset.active

    Array.from(heroBriefs[0].children).forEach( (brief, index) => {        
        if(index == startIndex){
            brief.dataset.active = true
        }
    })

    startIndex += 1

    if(startIndex == 3){
        startIndex = 0
    }
}, 1500)

// revealing verticles cdetails

const revealFunction = (btn) => {
    btn.closest(".verticle-card").querySelector(".verticle-detail").classList.toggle("reveal-detail")
    
} 

// hiding the verticles details

const verticleClose = document.querySelectorAll(".close")

Array.from(verticleClose).forEach( btn => {
    btn.addEventListener("click", () => {
        btn.closest(".verticle-detail").classList.remove("reveal-detail")
    })
})

// testimonial slider







const controlBtnsOne = document.querySelector("#one")

const controlBtnsTwo = document.querySelector("#two")

const controlBtnsThree = document.querySelector("#three")

const allBtns = document.querySelector(".control-btns")



controlBtnsOne.addEventListener("click", () => {
    const activeBtn = allBtns.querySelector("[data-active-btn]")
    const slider = document.querySelector(".carousel-inner")
    slider.style.transform = "translate(0)"
    delete activeBtn.dataset.activeBtn
    controlBtnsOne.dataset.activeBtn = true
})

controlBtnsTwo.addEventListener("click", () => {
    const activeBtn = allBtns.querySelector("[data-active-btn]")
    const slider = document.querySelector(".carousel-inner")
    slider.style.transform = "translate(-33.33%)"
    delete activeBtn.dataset.activeBtn
    controlBtnsTwo.dataset.activeBtn = true
})

controlBtnsThree.addEventListener("click", () => {
    const activeBtn = allBtns.querySelector("[data-active-btn]")
    const slider = document.querySelector(".carousel-inner")
    slider.style.transform = "translate(-66.66%)"
    delete activeBtn.dataset.activeBtn
    controlBtnsThree.dataset.activeBtn = true
})

/*Array.from(controlBtns).forEach( (btn, index) => {
    transformBy = index * index
    slider.style.transform = `translate(${-transformBy}%)`
})*/

// adding copyright

const year = new Date().getFullYear()

document.querySelector("#year").innerHTML = year
