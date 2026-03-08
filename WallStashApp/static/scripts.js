$(function() {
    $("#datepicker").datepicker({
    dateFormat: 'yy-mm-dd',
    onSelect: function(dateText) {
                window.location.href = `/list/date/${dateText}`;
              }
    });
});

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
    .then(() => {
    console.log('Text copied to clipboard!');
    })
    .catch(err => {
  console.error('Failed to copy:', err);
 });
}