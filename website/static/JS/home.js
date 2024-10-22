// console.log("Hello from Home")
function droplogic(){
    var dropdown = document.getElementById("language").value
    const eng_div = document.getElementById("engcontainer");
    const hin_div = document.getElementById("hincontainer");
    const pun_div = document.getElementById("puncontainer");
    
    console.log(dropdown);


    if(dropdown == 'English'){
        eng_div.style.display = 'flex';
        hin_div.style.display = 'none';
        pun_div.style.display = 'none';
        // eng.classList.add('show');
    }
    else if(dropdown == 'Hindi'){
        hin_div.style.display = 'flex';
        eng_div.style.display = 'none';
        pun_div.style.display = 'none';
        // eng.classList.add('show');
    }
    else if(dropdown == 'Punjabi'){
        pun_div.style.display = 'flex';
        hin_div.style.display = 'none';
        eng_div.style.display = 'none';
        // eng.classList.add('show');
    }
    else if(dropdown == 'All'){
        eng_div.style.display = 'flex';
        hin_div.style.display = 'flex';
        pun_div.style.display = 'flex';
        // eng.classList.add('show');
    }
    else{
        eng_div.style.display = 'none';
        hin_div.style.display = 'none';
        pun_div.style.display = 'none';
        // eng.classList.remove('show');
    }
}