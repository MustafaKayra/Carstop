$(function () {
  $("#datepicker").datepicker();
});

$(".clockpicker").clockpicker();

$.fn.datepicker.dates["en"] = {
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  today: "Today",
  clear: "Clear",
  format: "mm/dd/yyyy",
  titleFormat: "MM yyyy" /* Leverages same syntax as 'format' */,
  weekStart: 0,
};