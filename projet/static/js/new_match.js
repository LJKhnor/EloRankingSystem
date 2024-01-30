/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggleDropdown() {
    console.log("Enter toggleDropdown method for :")
    let elButtonId = event.currentTarget.id
    document.getElementById(elButtonId).classList.toggle("show");
}

//function searchLeague(){
//    let sel = document.getElementById("dropdown-league-choice-button");
//    if(!sel.classList.contains('show')){
//        let opt1 = document.createElement("option");
//        opt1.value = "League 2024"
//        opt1.text = "League 2024"
//        sel.add(opt1,null)
//    }
//}
