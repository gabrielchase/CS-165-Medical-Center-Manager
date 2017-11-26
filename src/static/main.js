console.log('load js')
$('#appointment-calendar').calendar({
    type: 'date',
    onChange: function (date, text, mode) {
        let url = window.location.href
        let n = url.indexOf('?');

        if (text && !n)  {
            url += `?d=${text}`
        } else if (n) {
            url = url.substring(0, n != -1 ? n : url.length);
            document.write(url);
            url += `?d=${text}`
        } 
        window.location.href = url
    },
})
console.log('done loading js')