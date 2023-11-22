function updateDateTime() {
    let dateTimeElement = document.getElementById('datetime');
    let now = new Date();
    
    // Format the date and time
    let formattedDateTime = now.getFullYear() + '-' +
                            ('0' + (now.getMonth() + 1)).slice(-2) + '-' +
                            ('0' + now.getDate()).slice(-2) + ' ' +
                            ('0' + now.getHours()).slice(-2) + ':' +
                            ('0' + now.getMinutes()).slice(-2) + ':' +
                            ('0' + now.getSeconds()).slice(-2);

    // Update the content of the element
    dateTimeElement.textContent = formattedDateTime;
  }

  // Update the date and time initially
  updateDateTime();

  // Update the date and time every second
  setInterval(updateDateTime, 1000);