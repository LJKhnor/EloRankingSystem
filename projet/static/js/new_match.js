/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggleDropdown() {
    console.log("Enter toggleDropdown method for :")
    let elButtonId = event.currentTarget.id
    document.getElementById(elButtonId.slice(0,-7)).classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.select')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function searchLeague(){
    let sel = document.getElementById("dropdown-league-choice-button");
    let opt1 = document.createElement("option");
    opt1.value = "League 2024"
    opt1.text = "League 2024"
    sel.add(opt1,null)
}

function onNewCreatedMatch(){
    console.log("coucou");
}