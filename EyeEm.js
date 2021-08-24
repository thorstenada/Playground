//var elements = document.querySelectorAll("button");   

var elements = document.querySelectorAll('[title*="Follow "]');
var x = document.querySelectorAll('[title*="Follow "]').length;

console.log(x);


for(var i = 0, len = elements.length; i < len; i++) {   
	 if (elements[i].innerText == "Follow"){
	   	//console.log("Button: " +  elements[i].id);
		// console.log("Button: " +  i);
	  	elements[i].click();
	}
}

elements = 0;
y = y+x;