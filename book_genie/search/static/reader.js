function set_category_value(category, anchor, value, text_field_value) {
    if (arguments.length < 4) {
	text_field_value = anchor.innerHTML;
    }
    if (arguments.length < 3) {
	value = anchor.innerHTML;
    }
    document.getElementById(category + '_btn').innerHTML = text_field_value + '<i class="icon-chevron-down"></i>';
    document.getElementById(category + '_text_field').value = text_field_value;
    document.getElementById(category + '_field').value = value;
}
