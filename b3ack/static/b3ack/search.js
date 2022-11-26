function searchFilter() {
	var input = document.getElementById("input");
	var filter = input.value.toUpperCase();
	var table = document.getElementById("table");
	var tr = table.getElementsByTagName("tr");

	// Go through every element in table
	for (var i = 1; i < tr.length; i++) {
		var td = tr[i].getElementsByTagName("td");
		var match = false;

		// Check if any of the attributes of the element match
		for (var j = 0; j < td.length; j++) {
			if (td[j]) {
				var txtValue = td[j].textContent || td[j].innerText;
				if (txtValue.toUpperCase().indexOf(filter) > -1) {
					tr[i].style.display = "";
					match = true;
					break;
				}
			}
		}

		// If no attributes match, don't display
		if (!match) {
			tr[i].style.display = "none";
		}
	}
}