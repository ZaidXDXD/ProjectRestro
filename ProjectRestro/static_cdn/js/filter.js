var filterButton = document.querySelector(".filter-button");
// console.log(filterButton);

var filterMenu = document.querySelector(".filter-menu");
// console.log(filterMenu);

var closeButton = document.querySelector(".close-container");

filterButton.addEventListener("click", () => {
	filterMenu.classList.add('show-filter');
})

filterButton.addEventListener("mouseover", () => {
	var filterIcon = document.querySelector(".filter-icon");
	console.log(filterIcon);
	filterIcon.src = `/static/img/Icons/black_filter_icon.png`;
})

filterButton.addEventListener("mouseout", () => {
	var filterIcon = document.querySelector(".filter-icon");
	console.log(filterIcon);
	filterIcon.src = `/static/img/Icons/white_filter_icon.png`;
})


closeButton.addEventListener("click", () => {
	filterMenu.classList.remove('show-filter');	
})

// -------------------------------------------------------------

function selectAllDishes(){
	var starterList = document.querySelectorAll('input[name="starter-checkbox"]');
	// console.log(starterList);
	var beverageList = document.querySelectorAll('input[name="beverage-checkbox"]');
	// console.log(beverageList);

	var maincourseList = document.querySelectorAll('input[name="main-course-checkbox"]');
	// console.log(maincourseList);

	var dessertList = document.querySelectorAll('input[name="dessert-checkbox"]');
	// console.log(dessertList);

	starterList.forEach( function(element, index) {
		if(!element.checked){
			element.click(); // checks the checkbox
		}
	});

	beverageList.forEach( function(element, index) {
		if(!element.checked){
			element.click(); // checks the checkbox
		}
	});

	maincourseList.forEach( function(element, index) {
		if(!element.checked){
			element.click(); // checks the checkbox
		}
	});

	dessertList.forEach( function(element, index) {
		if(!element.checked){
			element.click(); // checks the checkbox
		}
	});
}

function changeTheState(){
	var checkBox = document.querySelector('#checkbox1');

	var chooseMenu = document.querySelectorAll(".choice");
	if(checkBox.checked){
		chooseMenu.forEach( function(element, index) {
			element.classList.remove("unclickable");
		});
	}else{
		chooseMenu.forEach( function(element, index) {
			element.classList.add("unclickable");

			selectAllDishes();
		});
	}
}

// ---------------------------------------------------------------


// these arrays stores what all tags are to be displayed
var starters = new Set();
var beverages = new Set();
var main_course = new Set();
var desserts = new Set();

function updateStarters(element){
	// console.log(element);
	if(element.checked){
		starters.add(element.value);
	}
	else{
		starters.delete(element.value);
	}
	// console.log(starters)
}

function updateBeverages(element){
	// console.log(element);
	if(element.checked){
		beverages.add(element.value);
	}
	else{
		beverages.delete(element.value);
	}
	// console.log(beverages)
}

function updateMainCourse(element){
	// console.log(element);
	if(element.checked){
		main_course.add(element.value);
	}
	else{
		main_course.delete(element.value);
	}
	// console.log(main_course)
}

function updateDesserts(element){
	// console.log(element);
	if(element.checked){
		desserts.add(element.value);
	}
	else{
		desserts.delete(element.value);
	}
	// console.log(desserts)
}

function updateLists(){
	var starterList = document.querySelectorAll('input[name="starter-checkbox"]');
	// console.log(starterList);
	var beverageList = document.querySelectorAll('input[name="beverage-checkbox"]');
	// console.log(beverageList);

	var maincourseList = document.querySelectorAll('input[name="main-course-checkbox"]');
	// console.log(maincourseList);

	var dessertList = document.querySelectorAll('input[name="dessert-checkbox"]');
	// console.log(dessertList);

	starterList.forEach( function(element, index) {
		updateStarters(element);
	});

	beverageList.forEach( function(element, index) {
		updateBeverages(element);
	});

	maincourseList.forEach( function(element, index) {
		updateMainCourse(element);
	});

	dessertList.forEach( function(element, index) {
		updateDesserts(element);
	});
}

// calling the update list function as soon as the page reloads
updateLists();

function updateDishes(){

	// removing all beverage dishes
	var container = document.querySelector(".beveragesContainer");

	var dish = container.querySelectorAll(".dishCard");
	
	dish.forEach( function(element, index) {
		if(beverages.has(element.getAttribute('name'))){
			element.style.display = 'inline-grid';
		}
		else{
			element.style.display = 'none';
		}
	});

	// removing all satrter dishes
	container = document.querySelector(".startersContainer");

	dish = container.querySelectorAll(".dishCard");
	dish.forEach( function(element, index) {
		if(starters.has(element.getAttribute('name'))){
			element.style.display = 'inline-grid';
		}
		else{
			element.style.display = 'none';
		}
	});

	// removing all main-course dishes
	container = document.querySelector(".maincourseContainer");

	dish = container.querySelectorAll(".dishCard");
	dish.forEach( function(element, index) {
		if(main_course.has(element.getAttribute('name'))){
			element.style.display = 'inline-grid';
		}
		else{
			element.style.display = 'none';
		}
	});

	// removing all dessert dishes
	container = document.querySelector(".dessertsContainer");

	dish = container.querySelectorAll(".dishCard");
	dish.forEach( function(element, index) {
		if(desserts.has(element.getAttribute('name'))){
			element.style.display = 'inline-grid';
		}
		else{
			element.style.display = 'none';
		}
	});

}