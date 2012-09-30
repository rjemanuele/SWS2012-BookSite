function set_category_value(category, anchor, value) {
    if (arguments.length == 2) {
	value = anchor.innerHTML;
    }
    document.getElementById(category + '_btn').innerHTML = value;
    document.getElementById(category + '_field').value = value;
}
