// const dataTag = document.querySelector('#dateTag')
// let dateTimeTeg = timeConvert(dataTag)

// function timeConvert(UNIX_timestamp){
//     let diffTime = getTimeZone();
//     let a = new Date((UNIX_timestamp.textContent) * 1000);
//     console.log(UNIX_timestamp.textContent);
//     let months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
//     let year = a.getFullYear();
//     let month = months[a.getMonth()];
//     let date = a.getDate();
//     let hour = a.getHours();
//     let min = a.getMinutes();
//     // var sec = a.getSeconds();
//     let time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min;
//     console.log(time);
//     dataTag.innerHTML = time;
//     return 'ok';
//   }

// function getTimeZone() {
// let timezone_offset_minutes = new Date().getTimezoneOffset();
// timezone_offset_minutes = timezone_offset_minutes == 0 ? 0 : -timezone_offset_minutes;
// return timezone_offset_minutes * 60;
// }